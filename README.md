# novel-assistant

小说创作辅助工程。当前提供最小可用的创作工程初始化 CLI，仅需 Python 3.11 标准库，无第三方依赖。

## 运行方式

```
python novel.py init <目录>
```

- 目标目录不存在（含多级父目录）时自动创建。
- 命令退出码为 0，stdout 逐一输出全部已创建路径（四个子目录与 novel.json）。

## 目录用途

初始化后目标目录结构如下：

- `manuscript/` — 正文草稿存放目录（如各章节文本）。
- `outline/` — 大纲目录（情节线、章节提纲）。
- `characters/` — 角色设定目录（人物卡、关系设定）。
- `notes/` — 笔记目录（设定集、资料、灵感记录）。

项目元数据写入 `novel.json`：

```json
{
  "format_version": 1,
  "project_name": "<目标目录基名>"
}
```

`format_version` 为整数格式版本（本版钉值 1）；`project_name` 为项目名，等于目标目录基名。多余键允许存在，向前兼容。

## 重复初始化行为

对已经初始化过的目录（已存在 `novel.json`）再次执行 `python novel.py init <目录>`：

- 退出码非 0，stderr 输出非空可读的拒绝原因；
- 目标目录完整内容零改动——不新建、不修改、不删除任何文件或目录，既有创作内容绝不被覆盖。

缺少目录参数时（`python novel.py init`）同样以非零退出，并输出 usage 用法信息，不产生任何文件副作用。

## 测试

```
python -m unittest discover -s tests
```

覆盖三条路径：初始化成功、重复初始化拒绝、缺少参数拒绝。
