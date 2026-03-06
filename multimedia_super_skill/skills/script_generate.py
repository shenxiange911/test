from __future__ import annotations
import argparse
from core.contracts import SkillResult, Artifact
from core.registry import register

@register("script.generate")
def run(ctx, params):
    user_need = params["user_need"]
    # TODO: replace with your LLM tool
    script = f"""广告短视频剧本（mock）
需求：{user_need}

分镜概要：
1) 开场：产品出现 + 氛围
2) 中景：模特使用产品
3) 特写：核心卖点展示
4) 结尾：Call to action
"""
    return SkillResult(ok=True, artifacts=[Artifact(type="text", value=script)], data={"script": script})

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--user-need", required=True)
    args = ap.parse_args()
    res = run({}, {"user_need": args.user_need})
    print(res.data["script"])

if __name__ == "__main__":
    main()
