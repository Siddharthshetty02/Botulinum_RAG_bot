# Deep Learning, Neural Networks, and Architecture

## 1. Artificial Neural Network (ANN) Basics

An Artificial Neural Network is composed of layers of artificial neurons (perceptrons) connected by weighted links.

### 1.1 Mathematical Model of a Neuron
For input vector $\mathbf{x} = [x_1, x_2, \dots, x_n]$, weight vector $\mathbf{w} = [w_1, w_2, \dots, w_n]$, and bias $b$:

$$z = \mathbf{w}^T \mathbf{x} + b = \sum_{i=1}^n w_i x_i + b$$
$$a = \sigma(z)$$

where $\sigma$ is a non-linear activation function.

### 1.2 Common Activation Functions
- **ReLU (Rectified Linear Unit)**: $f(z) = \max(0, z)$. Fast, mitigates vanishing gradient problem for positive inputs.
- **Leaky ReLU**: $f(z) = \max(\alpha z, z)$ with small $\alpha \approx 0.01$. Prevents dying ReLU neurons.
- **Sigmoid**: $\sigma(z) = \frac{1}{1 + e^{-z}}$. Maps outputs to $(0, 1)$, ideal for binary classification probabilities.
- **Softmax**: $\sigma(\mathbf{z})_i = \frac{e^{z_i}}{\sum_{j} e^{z_j}}$. Converts raw logits into probability distribution over $K$ classes.
- **GELU (Gaussian Error Linear Unit)**: Smoother variant used extensively in Transformers (BERT, GPT).

---

## 2. Backpropagation & Optimization

### 2.1 Backpropagation
Backpropagation computes the gradient of the loss function $L$ with respect to each weight using the mathematical **Chain Rule**:

$$\frac{\partial L}{\partial w_{ij}^{(l)}} = \frac{\partial L}{\partial a_j^{(l)}} \cdot \frac{\partial a_j^{(l)}}{\partial z_j^{(l)}} \cdot \frac{\partial z_j^{(l)}}{\partial w_{ij}^{(l)}}$$

### 2.2 Optimization Algorithms
- **Stochastic Gradient Descent (SGD)**: Updates weights using mini-batches: $w \leftarrow w - \eta \nabla L(w)$.
- **Momentum**: Accelerates SGD along directions of consistent gradient by maintaining velocity $v_t = \beta v_{t-1} + (1-\beta) \nabla L$.
- **RMSprop**: Adapts learning rate per parameter by dividing by running average of squared gradients.
- **Adam (Adaptive Moment Estimation)**: Combines Momentum and RMSprop, maintaining first moment $m_t$ and second moment $v_t$ with bias correction. Default choice for modern deep learning.

---

## 3. Major Neural Network Architectures

### 3.1 Convolutional Neural Networks (CNNs)
- Designed for spatial/image grid data.
- **Core Operations**: Convolutional layers (extract local features via kernel sliding), Pooling layers (Max/Average pooling downsample feature maps), Fully Connected layers (final classification).
- **Key Architectures**: ResNet (Residual Connections solve gradient vanishing), EfficientNet, Vision Transformers (ViT).

### 3.2 Recurrent Neural Networks (RNNs) & LSTMs
- Designed for sequential time-series and natural language.
- **LSTMs (Long Short-Term Memory)**: Introduce Memory Cell $C_t$ and 3 gates (Forget Gate $f_t$, Input Gate $i_t$, Output Gate $o_t$) to solve the vanishing gradient problem over long sequences.

### 3.3 Transformer Architecture & Self-Attention
- Introduced in "Attention Is All You Need" (Vaswani et al., 2017). Replaced recurrent networks for NLP and GenAI.
- **Scaled Dot-Product Attention**:
  $$\text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V$$
  where $Q$ (Query), $K$ (Key), and $V$ (Value) are projections of input embeddings, and $d_k$ is key dimension.
- **Multi-Head Attention**: Runs multiple attention layers (heads) in parallel to capture distinct relationships across token sequences.
- **Foundational Models**: GPT (Decoder-only for generation), BERT (Encoder-only for embeddings & classification), T5/BART (Encoder-Decoder).
