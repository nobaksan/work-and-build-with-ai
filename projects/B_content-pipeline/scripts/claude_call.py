"""Claude Code CLI 를 그대로 부른다.

책의 독자가 터미널에서 하는 일과 같은 것을 스크립트가 대신 한다.
별도의 API 키가 필요 없다는 것이 이 방식의 장점이다.
"""
import subprocess

CLI = 'claude'


def ask(prompt, timeout=420):
    """프롬프트를 넘기고 답을 문자열로 받는다."""
    r = subprocess.run([CLI, '-p', prompt],
                       capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f'claude 실행 실패 (코드 {r.returncode})\n{r.stderr[:400]}')
    return r.stdout.strip()
