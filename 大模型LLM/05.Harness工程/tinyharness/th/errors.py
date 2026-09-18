"""CH9 · 错误处理与循环卫生。

核心原则：错误即上下文——把失败格式化成模型能读懂、能据以纠错的文本，
而不是抛异常崩溃。循环卫生：只记"失败"的重复调用，防止空转烧钱。
"""


def format_tool_error(exc: Exception) -> str:
    """把工具执行异常格式化成高信号反馈（回写给模型）。"""
    if isinstance(exc, TypeError):
        return f"[参数错误] {exc}，请检查参数类型与必填项。"
    if isinstance(exc, FileNotFoundError):
        return f"[文件不存在] {exc}，请先确认路径。"
    if isinstance(exc, PermissionError):
        return f"[权限拒绝] {exc}"
    return f"[执行失败] {type(exc).__name__}: {exc}"


class LoopHygiene:
    """循环卫生：只记录最近'失败'的 (tool, args)，成功即清零。

    评审修正点：不能把'连续 N 次相同调用'一律判为死循环——
    连续成功读同一文件是正常的。只有连续失败才该拦。
    """

    def __init__(self, threshold: int = 3, window: int = 6):
        self.threshold = threshold
        self.window = window
        self._fails: list[str] = []

    def is_stuck(self, sig: str) -> bool:
        return self._fails.count(sig) >= self.threshold

    def record_fail(self, sig: str) -> None:
        self._fails.append(sig)
        self._fails[:] = self._fails[-self.window:]

    def record_success(self, sig: str) -> None:
        self._fails[:] = [s for s in self._fails if s != sig]
