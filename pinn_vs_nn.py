import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

print("Starting the NN vs. PINN comparison with restricted training data (extrapolation test).")
print("This process may take a few minutes...")

# For reproducibility
torch.manual_seed(42)
np.random.seed(42)

# --- 1. Problem Definition and Data Generation (ADJUSTED) ---
k = 0.5  # Rate constant
A0 = 1.0 # Initial concentration

# Analytical solution (ground truth)
def analytical_solution(t):
    return A0 * np.exp(-k * t)

# Time domain
t_min, t_max = 0.0, 10.0
# KEY POINT: Training data only covers the first half of the time domain
t_max_train = t_max / 2.0 

# Training Data: only in the first half of the domain
n_train_points = 8
t_train_np = np.linspace(t_min, t_max_train, n_train_points)
A_train_np = analytical_solution(t_train_np) + 0.03 * np.random.randn(n_train_points)
A_train_np[0] = A0 

t_train = torch.tensor(t_train_np).float().view(-1, 1)
A_train = torch.tensor(A_train_np).float().view(-1, 1)

# Collocation Points: cover the ENTIRE DOMAIN to enforce physics everywhere
n_physics_points = 100
t_physics = torch.linspace(t_min, t_max, n_physics_points).view(-1, 1).requires_grad_(True)

# Test Data: cover the ENTIRE DOMAIN to plot the final curve
t_test = torch.linspace(t_min, t_max, 300).view(-1, 1)


# --- 2. Network Architectures (unchanged) ---
def create_network():
    return nn.Sequential(
        nn.Linear(1, 20), nn.Tanh(),
        nn.Linear(20, 20), nn.Tanh(),
        nn.Linear(20, 20), nn.Tanh(),
        nn.Linear(20, 1)
    )

# --- 3. Training the Standard Neural Network (NN) (unchanged) ---
print("\n--- Training the Standard Neural Network (NN) ---")
nn_model = create_network()
optimizer_nn = torch.optim.Adam(nn_model.parameters(), lr=1e-3)
loss_fn_nn = nn.MSELoss()
epochs = 20000 # Increased epochs to give the NN the best possible chance

for epoch in range(epochs):
    optimizer_nn.zero_grad()
    A_pred = nn_model(t_train)
    loss = loss_fn_nn(A_pred, A_train)
    loss.backward()
    optimizer_nn.step()
    if (epoch + 1) % 4000 == 0:
        print(f'NN Epoch [{epoch+1}/{epochs}], Loss: {loss.item():.6f}')

# --- 4. Training the PINN (logic unchanged) ---
print("\n--- Training the Physics-Informed Neural Network (PINN) ---")
pinn_model = create_network()
optimizer_pinn = torch.optim.Adam(pinn_model.parameters(), lr=1e-3)
epochs_pinn = 20000

for epoch in range(epochs_pinn):
    optimizer_pinn.zero_grad()
    A_pred_data = pinn_model(t_train)
    loss_data = loss_fn_nn(A_pred_data, A_train)
    A_pred_physics = pinn_model(t_physics)
    dA_dt = torch.autograd.grad(A_pred_physics, t_physics, grad_outputs=torch.ones_like(A_pred_physics), create_graph=True)[0]
    residual = dA_dt + k * A_pred_physics
    loss_physics = torch.mean(residual**2)
    loss = loss_data + loss_physics
    loss.backward()
    optimizer_pinn.step()
    if (epoch + 1) % 4000 == 0:
        print(f'PINN Epoch [{epoch+1}/{epochs_pinn}], Loss: {loss.item():.6f} (Data: {loss_data.item():.6f}, Physics: {loss_physics.item():.6f})')

# --- 5. Generating Predictions for Animation (unchanged) ---
nn_model.eval()
pinn_model.eval()
with torch.no_grad():
    A_pred_nn = nn_model(t_test).numpy()
    A_pred_pinn = pinn_model(t_test).numpy()

t_test_np = t_test.numpy()
A_real_np = analytical_solution(t_test_np)

# --- 6. Creating the Animation (visuals adjusted) ---
print("\n--- Generating the animation 'pinn_vs_nn_extrapolation.gif' ---")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7), sharey=True)
fig.suptitle("Extrapolation Test: Standard NN vs. PINN", fontsize=18)

# Plot 1 Setup: Standard NN
ax1.set_title("1. NN: Fails catastrophically to extrapolate", fontsize=14)
ax1.set_xlabel("Time (s)", fontsize=12)
ax1.set_ylabel("Concentration [A]", fontsize=12)
ax1.set_xlim(t_min, t_max)
ax1.set_ylim(-0.2, 1.2) # Fixed y-limit to see the NN's failure
ax1.plot(t_test_np, A_real_np, color='lightgray', linestyle='--', label='Real Process', lw=2)
ax1.plot(t_train_np, A_train_np, 'o', color='k', markerfacecolor='none', markersize=8, label='Training Data')
line_nn, = ax1.plot([], [], color='steelblue', label='NN Prediction', lw=2.5)
# Add a vertical line to mark the extrapolation zone
ax1.axvline(t_max_train, color='r', linestyle='--', alpha=0.8, label='Extrapolation Start')
ax1.legend(loc='upper right')
ax1.grid(True, linestyle=':', alpha=0.6)

# Plot 2 Setup: PINN
ax2.set_title("2. PINN: Successfully extrapolates using physics", fontsize=14)
ax2.set_xlabel("Time (s)", fontsize=12)
ax2.set_xlim(t_min, t_max)
ax2.plot(t_test_np, A_real_np, color='lightgray', linestyle='--', label='Real Process', lw=2)
ax2.plot(t_train_np, A_train_np, 'o', color='k', markerfacecolor='none', markersize=8, label='Training Data')
line_pinn, = ax2.plot([], [], color='teal', label='PINN Prediction', lw=2.5)
# Add the vertical line
ax2.axvline(t_max_train, color='r', linestyle='--', alpha=0.8, label='Extrapolation Start')
ax2.legend(loc='upper right')
ax2.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout(rect=[0, 0.03, 1, 0.95])

total_frames = 150

def update(frame):
    # Usando (frame + 1) para garantir que a animação chegue a 100% no final
    max_index = int(((frame + 1) / total_frames) * len(t_test_np))
    
    # Garante que max_index não exceda o limite do array
    max_index = min(max_index, len(t_test_np))

    line_nn.set_data(t_test_np[:max_index], A_pred_nn[:max_index])
    line_pinn.set_data(t_test_np[:max_index], A_pred_pinn[:max_index])
    return line_nn, line_pinn

# A mudança crucial: blit=False torna a animação mais robusta
ani = FuncAnimation(fig, update, frames=total_frames, interval=30, blit=False)
ani.save('pinn_vs_nn_extrapolation.gif', writer='pillow', fps=30)

print("\nAnimation 'pinn_vs_nn_extrapolation.gif' saved successfully!")
