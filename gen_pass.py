import hashlib, os, binascii

print("=== 🔐 Zero-Knowledge Auth 密文生成器 ===")
pwd = input("请输入你想设置的监视器密码: ")

# 1. 前端计算
client_key = hashlib.sha256(pwd.encode()).hexdigest()

# 2. 生成随机盐
salt = binascii.hexlify(os.urandom(8)).decode()

# 3. 后端计算
final_hash = hashlib.sha256((salt + client_key).encode()).hexdigest()

print("\n✅ 生成成功！请将下面这行完整代码复制，并替换掉 server.conf 里的 admin_key：\n")
print("-" * 60)
print(f"admin_key={salt}${final_hash}")
print("-" * 60)
print("\n(替换完成后，就算 server.conf 被全网公开也绝对安全！)")

# === [新增] 防止程序闪退，等待用户手动按回车退出 ===
input("\n复制完成后，请按回车键 (Enter) 退出程序...")