# 渐进式加载 多用代码执行
"""
OpenClaw
src/agents/skills/
    code-review/
        manifest.json   <- 技能描述、触发条件
        prompt.md       <- 技能专用的系统指令
        tools.ts        <- 技能专属工具（可选）
    security-audit/
        manifest.json
        prompt.md

manifest.json
{
    "name": "code-review",
    "description": "审查代码变更，检查安全问题和最佳实践",
    "triggers": ["review", "审查", "看看这段代码"],
    "requiredTools": ["Read", "Grep", "Bash"]
}
"""