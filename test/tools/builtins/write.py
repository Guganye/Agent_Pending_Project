from pathlib import Path
from typing import Optional


def write_file(path: str, content: str, cwd: Optional[str] = None) -> str:
    """
    写入内容到文件。自动创建父目录。

    Args:
        path: 文件路径（相对或绝对）
        content: 要写入的内容
        cwd: 工作目录

    Returns:
        成功消息
    """
    if cwd:
        file_path = Path(cwd) / path
    else:
        file_path = Path(path)

    file_path = file_path.resolve()

    # 创建父目录
    file_path.parent.mkdir(parents=True, exist_ok=True)

    # 写入文件
    file_path.write_text(content, encoding="utf-8")

    return f"Successfully wrote {len(content)} bytes to {path}"