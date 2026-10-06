# snapshot-compact

由 tick 驱动的快照压缩模拟：逐 tick 摄入增量，压缩时把增量并进基准视图，只保留窗口内的压缩记录。只用 Python 标准库。

```
python3 -m unittest discover -s tests
python3 -m snapcompact --sample=order
python3 -m snapcompact --sample=future
python3 -m snapcompact --sample=idem
python3 -m snapcompact --sample=retention
python3 -m snapcompact --sample=work
```

## 口径

- **增量合并**：一次压缩把截至当前 tick 的所有未合并增量并进基准视图，同一键按 tick 先后，晚者覆盖早者。
- **时间边界**：tick 晚于当前时刻的增量不参与本次压缩，留到以后。
- **幂等**：同一个压缩单号重复执行是空操作，不新增压缩记录。
- **保留窗口**：压缩记录只保留 tick 落在 `[当前 tick - 窗口, 当前 tick]` 内的那些。

## 不变量

- 基准视图里同一键的值等于截止时刻最后一次写入的值。
- 压缩记录按 tick 非降序，条数不超过窗口内的 tick 数。
- `scanned` 不随压缩次数平方级放大：两千次压缩的 `scanned` 不超过 6000。

## 输出契约

每个场景打印一行 JSON：`order` 给 `{"x": <值>}`，`future` 给 `{"keys": [...]}`，
`idem` / `retention` 给 `{"history": N}`，`work` 给 `{"compacts": N, "scanned": N}`。
状态键固定为 `merged` / `deltas` / `applied` / `compactions` / `history`。
