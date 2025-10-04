import os
import random
import time
from dataclasses import dataclass
from collections import namedtuple

import gymnasium as gym
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import tyro
from torch.distributions.categorical import Categorical
from torch.utils.tensorboard import SummaryWriter
import torch.onnx

# --- START: Custom Replay Buffer (cleanrl-free) ---

# A named tuple to hold the batch of data sampled from the buffer
ReplayBufferSamples = namedtuple(
    "ReplayBufferSamples",
    ("observations", "actions", "next_observations", "dones", "rewards"),
)

class ReplayBuffer:
    """A simple replay buffer implementation."""
    def __init__(
        self,
        buffer_size,
        observation_space,
        action_space,
        device,
        handle_timeout_termination=True, # This argument is kept for compatibility but not used in this simple version
    ):
        self.buffer_size = buffer_size
        self.device = device
        self.obs_shape = observation_space.shape
        
        self.observations = np.zeros((self.buffer_size,) + self.obs_shape, dtype=observation_space.dtype)
        self.actions = np.zeros((self.buffer_size,) + action_space.shape, dtype=action_space.dtype)
        self.rewards = np.zeros((self.buffer_size,), dtype=np.float32)
        self.dones = np.zeros((self.buffer_size,), dtype=np.float32)
        self.next_observations = np.zeros((self.buffer_size,) + self.obs_shape, dtype=observation_space.dtype)
        
        self.pos = 0
        self.full = False

    def add(self, obs, next_obs, action, reward, done, infos):
        self.observations[self.pos] = np.array(obs).copy()
        self.actions[self.pos] = np.array(action).copy()
        self.rewards[self.pos] = np.array(reward).copy()
        self.dones[self.pos] = np.array(done).copy()
        self.next_observations[self.pos] = np.array(next_obs).copy()
        
        self.pos += 1
        if self.pos == self.buffer_size:
            self.full = True
            self.pos = 0

    def sample(self, batch_size: int):
        """Sample a batch of transitions from the buffer."""
        # Determine the current size of the buffer
        current_size = self.buffer_size if self.full else self.pos
        
        # Sample random indices
        batch_inds = np.random.randint(0, current_size, size=batch_size)
        
        # Retrieve the data
        obs = self.observations[batch_inds]
        actions = self.actions[batch_inds]
        rewards = self.rewards[batch_inds]
        dones = self.dones[batch_inds]
        next_obs = self.next_observations[batch_inds]
        
        # Convert to PyTorch tensors and move to the correct device
        obs_tensor = torch.as_tensor(obs, device=self.device)
        actions_tensor = torch.as_tensor(actions, device=self.device)
        rewards_tensor = torch.as_tensor(rewards, device=self.device).flatten()
        dones_tensor = torch.as_tensor(dones, device=self.device).flatten()
        next_obs_tensor = torch.as_tensor(next_obs, device=self.device)
        
        return ReplayBufferSamples(
            observations=obs_tensor,
            actions=actions_tensor,
            rewards=rewards_tensor,
            dones=dones_tensor,
            next_observations=next_obs_tensor,
        )

# --- END: Custom Replay Buffer ---


@dataclass
class Args:
    exp_name: str = os.path.basename(__file__)[: -len(".py")]
    """the name of this experiment"""
    seed: int = 1
    """seed of the experiment"""
    torch_deterministic: bool = True
    """if toggled, `torch.backends.cudnn.deterministic=False`"""
    cuda: bool = True
    """if toggled, cuda will be enabled by default"""
    track: bool = False
    """if toggled, this experiment will be tracked with Weights and Biases"""
    wandb_project_name: str = "cleanRL"
    """the wandb's project name"""
    wandb_entity: str = None
    """the entity (team) of wandb's project"""
    capture_video: bool = False
    """whether to capture videos of the agent performances (check out `videos` folder)"""

    # Algorithm specific arguments
    env_id: str = "CartPole-v1"
    """the id of the environment"""
    total_timesteps: int = 25000
    """total timesteps of the experiments"""
    buffer_size: int = int(1e4)
    """the replay memory buffer size"""
    gamma: float = 0.99
    """the discount factor gamma"""
    tau: float = 1.0
    """target smoothing coefficient (default: 1)"""
    batch_size: int = 128
    """the batch size of sample from the reply memory"""
    learning_starts: int = 1000
    """timestep to start learning"""
    policy_lr: float = 3e-4
    """the learning rate of the policy network optimizer"""
    q_lr: float = 1e-3
    """the learning rate of the Q network network optimizer"""
    update_frequency: int = 1
    """the frequency of training updates"""
    target_network_frequency: int = 500
    """the frequency of updates for the target networks"""
    alpha: float = 0.2
    """Entropy regularization coefficient."""
    autotune: bool = True
    """automatic tuning of the entropy coefficient"""
    target_entropy_scale: float = 0.89
    """coefficient for scaling the autotune entropy target"""


def make_env(env_id, seed, idx, capture_video, run_name):
    """Simplified environment creation for non-Atari envs."""
    def thunk():
        if capture_video and idx == 0:
            env = gym.make(env_id, render_mode="rgb_array")
            env = gym.wrappers.RecordVideo(env, f"videos/{run_name}")
        else:
            env = gym.make(env_id)
        env = gym.wrappers.RecordEpisodeStatistics(env)
        env.action_space.seed(seed)
        return env

    return thunk


def layer_init(layer, bias_const=0.0):
    nn.init.kaiming_normal_(layer.weight)
    torch.nn.init.constant_(layer.bias, bias_const)
    return layer


# ALGO LOGIC: initialize agent here:
# MLP architecture for vector-based observations
class SoftQNetwork(nn.Module):
    def __init__(self, envs):
        super().__init__()
        self.net = nn.Sequential(
            layer_init(nn.Linear(np.array(envs.single_observation_space.shape).prod(), 256)),
            nn.ReLU(),
            layer_init(nn.Linear(256, 256)),
            nn.ReLU(),
            layer_init(nn.Linear(256, envs.single_action_space.n)),
        )

    def forward(self, x):
        return self.net(x)


class Actor(nn.Module):
    def __init__(self, envs):
        super().__init__()
        self.net = nn.Sequential(
            layer_init(nn.Linear(np.array(envs.single_observation_space.shape).prod(), 256)),
            nn.ReLU(),
            layer_init(nn.Linear(256, 256)),
            nn.ReLU(),
            layer_init(nn.Linear(256, envs.single_action_space.n)),
        )

    def forward(self, x):
        return self.net(x)

    def get_action(self, x):
        logits = self(x)
        policy_dist = Categorical(logits=logits)
        action = policy_dist.sample()
        # Action probabilities for calculating the adapted soft-Q loss
        action_probs = policy_dist.probs
        log_prob = F.log_softmax(logits, dim=1)
        return action, log_prob, action_probs


if __name__ == "__main__":
    args = tyro.cli(Args)
    run_name = f"{args.env_id}__{args.exp_name}__{args.seed}__{int(time.time())}"
    if args.track:
        import wandb

        wandb.init(
            project=args.wandb_project_name,
            entity=args.wandb_entity,
            sync_tensorboard=True,
            config=vars(args),
            name=run_name,
            monitor_gym=True,
            save_code=True,
        )
    writer = SummaryWriter(f"runs/{run_name}")
    writer.add_text(
        "hyperparameters",
        "|param|value|\n|-|-|\n%s" % ("\n".join([f"|{key}|{value}|" for key, value in vars(args).items()])),
    )

    # TRY NOT TO MODIFY: seeding
    random.seed(args.seed)
    np.random.seed(args.seed)
    torch.manual_seed(args.seed)
    torch.backends.cudnn.deterministic = args.torch_deterministic

    device = torch.device("cuda" if torch.cuda.is_available() and args.cuda else "cpu")

    # env setup
    envs = gym.vector.SyncVectorEnv([make_env(args.env_id, args.seed, 0, args.capture_video, run_name)])
    assert isinstance(envs.single_action_space, gym.spaces.Discrete), "only discrete action space is supported"

    actor = Actor(envs).to(device)
    qf1 = SoftQNetwork(envs).to(device)
    qf2 = SoftQNetwork(envs).to(device)
    qf1_target = SoftQNetwork(envs).to(device)
    qf2_target = SoftQNetwork(envs).to(device)
    qf1_target.load_state_dict(qf1.state_dict())
    qf2_target.load_state_dict(qf2.state_dict())
    # TRY NOT TO MODIFY: eps=1e-4 increases numerical stability
    q_optimizer = optim.Adam(list(qf1.parameters()) + list(qf2.parameters()), lr=args.q_lr, eps=1e-4)
    actor_optimizer = optim.Adam(list(actor.parameters()), lr=args.policy_lr, eps=1e-4)

    # Automatic entropy tuning
    if args.autotune:
        target_entropy = -args.target_entropy_scale * torch.log(1 / torch.tensor(envs.single_action_space.n))
        log_alpha = torch.zeros(1, requires_grad=True, device=device)
        alpha = log_alpha.exp().item()
        a_optimizer = optim.Adam([log_alpha], lr=args.q_lr, eps=1e-4)
    else:
        alpha = args.alpha

    rb = ReplayBuffer(
        args.buffer_size,
        envs.single_observation_space,
        envs.single_action_space,
        device,
        handle_timeout_termination=True,
    )
    start_time = time.time()

    # TRY NOT TO MODIFY: start the game
    obs, _ = envs.reset(seed=args.seed)
    for global_step in range(args.total_timesteps):
        # ALGO LOGIC: put action logic here
        if global_step < args.learning_starts:
            actions = np.array([envs.single_action_space.sample() for _ in range(envs.num_envs)])
        else:
            actions, _, _ = actor.get_action(torch.Tensor(obs).to(device))
            actions = actions.detach().cpu().numpy()

        # TRY NOT TO MODIFY: execute the game and log data.
        next_obs, rewards, terminations, truncations, infos = envs.step(actions)

        # TRY NOT TO MODIFY: record rewards for plotting purposes
        if "final_info" in infos:
            for info in infos["final_info"]:
                print(f"global_step={global_step}, episodic_return={info['episode']['r']}")
                writer.add_scalar("charts/episodic_return", info["episode"]["r"], global_step)
                writer.add_scalar("charts/episodic_length", info["episode"]["l"], global_step)
                break

        # TRY NOT TO MODIFY: save data to reply buffer; handle `final_observation`
        real_next_obs = next_obs.copy()
        for idx, trunc in enumerate(truncations):
            if trunc:
                real_next_obs[idx] = infos["final_observation"][idx]
        rb.add(obs, real_next_obs, actions, rewards, terminations, infos)

        # TRY NOT TO MODIFY: CRUCIAL step easy to overlook
        obs = next_obs

        # ALGO LOGIC: training.
        if global_step > args.learning_starts:
            if global_step % args.update_frequency == 0:
                data = rb.sample(args.batch_size)
                # CRITIC training
                with torch.no_grad():
                    _, next_state_log_pi, next_state_action_probs = actor.get_action(data.next_observations)
                    qf1_next_target = qf1_target(data.next_observations)
                    qf2_next_target = qf2_target(data.next_observations)
                    # we can use the action probabilities instead of MC sampling to estimate the expectation
                    min_qf_next_target = next_state_action_probs * (
                        torch.min(qf1_next_target, qf2_next_target) - alpha * next_state_log_pi
                    )
                    # adapt Q-target for discrete Q-function
                    min_qf_next_target = min_qf_next_target.sum(dim=1)
                    next_q_value = data.rewards.flatten() + (1 - data.dones.flatten()) * args.gamma * (min_qf_next_target)

                # use Q-values only for the taken actions
                qf1_values = qf1(data.observations)
                qf2_values = qf2(data.observations)
                qf1_a_values = qf1_values.gather(1, data.actions.long().unsqueeze(1)).view(-1)
                qf2_a_values = qf2_values.gather(1, data.actions.long().unsqueeze(1)).view(-1)
                qf1_loss = F.mse_loss(qf1_a_values, next_q_value)
                qf2_loss = F.mse_loss(qf2_a_values, next_q_value)
                qf_loss = qf1_loss + qf2_loss

                q_optimizer.zero_grad()
                qf_loss.backward()
                q_optimizer.step()

                # ACTOR training
                _, log_pi, action_probs = actor.get_action(data.observations)
                with torch.no_grad():
                    qf1_values = qf1(data.observations)
                    qf2_values = qf2(data.observations)
                    min_qf_values = torch.min(qf1_values, qf2_values)
                # no need for reparameterization, the expectation can be calculated for discrete actions
                actor_loss = (action_probs * ((alpha * log_pi) - min_qf_values)).mean()

                actor_optimizer.zero_grad()
                actor_loss.backward()
                actor_optimizer.step()

                if args.autotune:
                    # reuse action probabilities for temperature loss
                    alpha_loss = (action_probs.detach() * (-log_alpha.exp() * (log_pi + target_entropy).detach())).mean()

                    a_optimizer.zero_grad()
                    alpha_loss.backward()
                    a_optimizer.step()
                    alpha = log_alpha.exp().item()

            # update the target networks
            if global_step % args.target_network_frequency == 0:
                for param, target_param in zip(qf1.parameters(), qf1_target.parameters()):
                    target_param.data.copy_(args.tau * param.data + (1 - args.tau) * target_param.data)
                for param, target_param in zip(qf2.parameters(), qf2_target.parameters()):
                    target_param.data.copy_(args.tau * param.data + (1 - args.tau) * target_param.data)

            if global_step % 100 == 0:
                writer.add_scalar("losses/qf1_values", qf1_a_values.mean().item(), global_step)
                writer.add_scalar("losses/qf2_values", qf2_a_values.mean().item(), global_step)
                writer.add_scalar("losses/qf1_loss", qf1_loss.item(), global_step)
                writer.add_scalar("losses/qf2_loss", qf2_loss.item(), global_step)
                writer.add_scalar("losses/qf_loss", qf_loss.item() / 2.0, global_step)
                writer.add_scalar("losses/actor_loss", actor_loss.item(), global_step)
                writer.add_scalar("losses/alpha", alpha, global_step)
                print("SPS:", int(global_step / (time.time() - start_time)))
                writer.add_scalar("charts/SPS", int(global_step / (time.time() - start_time)), global_step)
                if args.autotune:
                    writer.add_scalar("losses/alpha_loss", alpha_loss.item(), global_step)

    # --- ONNX EXPORT ---
    # After training, export the actor model to ONNX format.
    model_path = f"runs/{run_name}/sac_cartpole_actor.onnx"
    # Ensure the directory exists
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    
    # Set the model to evaluation mode
    actor.eval()
    
    # Create a dummy input with the correct shape
    dummy_input = torch.randn(1, *envs.single_observation_space.shape, device=device)
    
    print(f"\nExporting model to {model_path}...")
    torch.onnx.export(
        actor,
        dummy_input,
        model_path,
        verbose=False,
        input_names=["observation"],
        output_names=["logits"],
        opset_version=11,
    )
    print("Model exported successfully! ✅")
    
    envs.close()
    writer.close()