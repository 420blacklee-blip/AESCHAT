import hashlib, os, binascii

def generate_key_string(key_name, prompt_text):
    pwd = input(f"请输入你想设置的【{prompt_text}】密码: ").strip()
    if not pwd:
        return None
    
    # 1. 前端计算模拟 (SHA256) - 这是触发 API 真正需要的 key 参数
    client_key = hashlib.sha256(pwd.encode()).hexdigest()

    # 2. 生成随机盐 (16位Hex)
    salt = binascii.hexlify(os.urandom(8)).decode()

    # 3. 后端计算 (Salt + Client_Key 的 SHA256) - 这是存入 server.conf 的密文
    final_hash = hashlib.sha256((salt + client_key).encode()).hexdigest()
    
    config_string = f"{key_name}={salt}${final_hash}"
    
    # 返回一个字典，包含配置文件字符串和用于 API 请求的 client_key
    return {
        "name": key_name,
        "config": config_string,
        "client_key": client_key
    }

print("=== 🔐 Zero-Knowledge Auth 多功能密钥与指令生成器 ===")
print("此工具将自动生成 server.conf 密文，以及对应的 PowerShell 触发指令！\n")

# [第一步]：获取主机地址用于生成最终的命令
host = input("第一步：请输入你的服务器外网域名/地址 (例如 https://wwww.xxx.com 不建议跳过-否则你无法使用高级指令): ").strip()
if host and host.endswith('/'):
    host = host[:-1]  # 移除末尾多余的斜杠

print("\n--- 开始生成密钥 ---")
results = []

# [第二步]：依次生成三个核心密钥
res_admin = generate_key_string("admin_key", "管理面板监控")
if res_admin: results.append(res_admin)

res_switch = generate_key_string("switch_key", "系统全局熔断")
if res_switch: results.append(res_switch)

res_room = generate_key_string("room_change_key", "全员强制空间跳跃")
if res_room: results.append(res_room)

print("\n" + "=" * 70)
if results:
    print("✅ [配置环节] 请将以下内容完整复制，并替换到 server.conf 文件对应的位置：\n")
    print("-" * 60)
    for r in results:
        print(r["config"])
    print("-" * 60)
    print("\n(替换完成后，请重启后端服务使配置生效)")
    
    # 筛选出属于应急控制的 key
    emergency_cmds = [r for r in results if r["name"] in ["switch_key", "room_change_key"]]
    
    # [第三步]：如果用户输入了 host，且生成了应急控制 key，则输出 PowerShell 命令
    if host and emergency_cmds:
        print("\n" + "=" * 70)
        print("🚀 [作战指令] 你的专属 PowerShell 紧急触发指令：")
        print("建议将以下命令保存在本地记事本中备用，在危急时刻直接粘贴到 PowerShell 中执行！\n")
        
        for r in emergency_cmds:
            if r["name"] == "switch_key":
                print("🔴 【全局熔断 / 恢复】(关门保护):")
            elif r["name"] == "room_change_key":
                print("🌀 【空间跳跃】(全员强制转移):")
            
            # 自动生成带有 ConvertTo-Json 的美化输出版命令
            print(f'Invoke-RestMethod -Uri "{host}/api/emergency?key={r["client_key"]}" -Method Get | ConvertTo-Json\n')
        print("=" * 70)
else:
    print("⚠️ 未输入任何密码，未生成新密钥。")

# === 防止 Windows 控制台双击运行闪退 ===
print("\n数据已全部输出，请确认已复制需要的内容。")
# 修正了控制台关闭的逻辑提示
input("请按回车键 (Enter) 退出程序...")
