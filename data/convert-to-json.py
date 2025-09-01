import json

def dx_process(block):
    dx_block = {}
    for k, v in block.items():
        if k.startswith('dx_'):
            new_key = k[3:]  # dx_を除去
            dx_block[new_key] = v
        else:
            dx_block[k] = v
    # titleの先頭に【DX】を追加
    if 'title' in dx_block:
        dx_block['title'] = '【DX】' + dx_block['title']
    return dx_block

input_path = 'music-ex.json'
output_path = 'music.json'

with open(input_path, encoding='utf-8') as f:
    data = json.load(f)

result = []

for block in data:
    has_lev_bas = any(key.startswith('lev_bas') for key in block)
    has_dx_lev_bas = any(key.startswith('dx_lev_bas') for key in block)

    # 1. 「dx_lev_bas」がない場合、そのまま転記
    if not has_dx_lev_bas:
        result.append(block)
    # 2. 「lev_bas」がない場合、そのまま転記し、dx_processを呼ぶ
    elif not has_lev_bas:
        result.append(dx_process(block))
    # 3. 両方ある場合
    elif has_lev_bas and has_dx_lev_bas:
        # lev_系だけ残す
        lev_block = {k: v for k, v in block.items() if not k.startswith('dx_')}
        # dx_系だけ残す
        dx_block = {k: v for k, v in block.items() if k.startswith('dx_') or not k.startswith('lev_')}
        result.append(lev_block)
        result.append(dx_process(dx_block))

with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"変換完了: {output_path}")