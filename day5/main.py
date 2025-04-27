import qrcode
import qrcode.constants

def generate_qr():
    # 入力を受け取る
    data = input("QRコードにしたい文字列またはURLを入力してください:")

    if not data:
        print("入力が空です.")
        return
    
    # QRコード生成
    img = qrcode.make(data)

    # ファイル名を決定
    filename = input("保存するファイル名を入力してください:")
    if not filename:
        filename = "qr_code"
    
    # 保存
    img.save(f"{filename}.png")
    print(f"QRコードを{filename}.pngとして保存しました")

if __name__ == "__main__":
    generate_qr()
