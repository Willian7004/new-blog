# LLM

本文介绍了一些LLM的测试数据，我使用的LLM以及使用体验。

| Model                     | AIME2024 | AIME2025   | GPQA Diamond | Codeforces(rating) | LiveCodeBench | SWE-Bench  | Humanity’s Last Exam | Frontier Math |
| ------------------------- | -------- | ---------- | ------------ | ------------------ | ------------- | ---------- | --------------------- | ------------- |
| Qwen3 1.7b                | 48.3     | 36.8       | 40.1         |                    | 33.2          |            |                       |               |
| Qwen3 4b                  | 73.8     | 65.6       | 55.9         | 1671               | 54.2          |            |                       |               |
| Areal boba2 8b            |          |            |              | 1962               | 63            |            |                       |               |
| Areal boba2 14b           |          |            |              | 2044               | 69.1          |            |                       |               |
| Ring Lite 16.8b a2.75b    | 76.6     | 69.1       | 61.1         |                    | 60.7          |            |                       |               |
| Deepseek R1 0528 Qwen3 8b | 86       | 76.3       | 61.1         |                    | 60.5          |            |                       |               |
| Deepseek R1 0528          | 91.4     | 87.5       | 81           |                    | 73.3          |            | 14                    |               |
| Gemini 2.5 Flash          |          | 72         | 82.8         |                    | 55.4          | 48.9(60.3) | 11                    |               |
| OpenAI o4 mini            | 93.4     |            | 81.4         | 2719               | 80.2          | 68.1       | 14.3                  | 17            |
| Grok3 mini Reasoning      | 90（96） |            | 81（84）     |                    | 66.7          |            |                       | 6             |
| Claude  Sonnet 4          |          | 70.5（85） | 75.4（83.8） |                    |               | 72.7(80.2) |                       |               |
| Gemini2.5 pro 0605        |          | 88         | 86.4         |                    | 69            | 59.6(67.2) | 21                    |               |
| MiMo VL 7B RL             | 67.5     | 52.5       | 58.3         |                    |               |            |                       |               |

### 模型测试数据

这部分收录了一些LLM在常见的测试集的测试结果，只收录同规模下最优秀的模型。

旗舰模型和推理模型：

多模态模型：

| Model                  | MMLU | MMNU-Pro | ChartQAPro | DocVQA | OCRBench | AI2D | MathVista | MathVision | Vibe Eval(Reka) |
| ---------------------- | ---- | -------- | ---------- | ------ | -------- | ---- | --------- | ---------- | --------------- |
| OpenAI o4 mini         | 81.6 |          |            |        |          |      | 84.4      |            |                 |
| Gemini2.5 Flash        | 79.7 |          |            |        |          |      |           |            | 65.4            |
| Gemini2.5 Pro          | 82   |          |            |        |          |      |           |            | 67.2            |
| Claude Sonnet4         | 74.4 |          |            |        |          |      |           |            |                 |
| Kimi VL 16b a2.8b 2506 | 64.0 | 46.3     |            |        |          |      | 80.1      | 56.9       |                 |
| MiMo VL 7b RL          | 66.7 | 46.2     | 53.6       | 95.7   | 86.6     | 83.5 | 81.5      | 60.4       |                 |
| GLM4.1V 9b Thinking    | 68.0 | 57.1     | 59.5       |        | 84.2     | 87.9 | 80.7      |            |                 |

无审查模型：

这类模型比较少没有专门的测试数据，通常与基底模型接近，目前Dolphin3系列比较完善，也可以选择最新模型的去对齐版本。

无审查模型在角色扮演等任务有优势，也可以用于处理成人等题材的内容。

### 模型推理

##### 推理框架

桌面端：

1. Transformers兼容性强，但优化较差。
2. Ollama基于llama.cpp，稳定性和显存优化较好，但对多模态模型的支持比上游慢。
3. LM Studio同样基于llama.cpp，兼容性与上游一致，提供图形界面并集成RAG功能。
4. VLLM注重张量并行和并发优化。
5. KTransformer注重异构计算，长上下文和并发速度相比CPU部署有一定优势。

移动端：
不少应用来源与其它推理框架，目前使用MNN Chat，可能是唯一对Omni模型支持较好的推理框架，但桌面端还没有完全适配（参考 https://github.com/alibaba/MNN/issues/3520 ）。

##### 本地部署情况

考虑模型适配和自带界面，我选择了LM Studio。我的电脑配置为3070m+5600h+双通道ddr4 3200。桌面端部署情况如下：

1. Deepseek R1 0528 Qwen3 8b用于通用任务。
2. Mimo VL 7b RL用于多模态任务。
3. Dolphin3.0 Llama3 8b用于无审查任务。
4. Ring Lite用于CPU推理。

手机配置为骁龙8gen1+8g内存，使用MNN Chat。移动端部署情况如下：

1. Qwen3 4b用于通用任务。
2. Qwen2.5 vl 3b用于多模态任务。
3. Qwen2.5 Omni 3b用于有语音输入的任务，TTS速度较慢。
（考虑到内存带宽瓶颈，16g设备用Ring Lite比较合适，待Llama.cpp支持后也可以用Kimi VL）

##### api使用情况

我个人偏向开源模型，使用的api如下：

1. Deepseek api，使用Deepseek模型，因为其模型在开源模型中比较优秀，成本也不太高。
2. Siliconflow api，以前Deepseek api繁忙时用于Deepseek模型，在Openrouter使用多账号策略后基本弃用。
3. Openrouter api，主要使用免费模型，提供Dolphin3等无审查模型相比国内api也有优势。
