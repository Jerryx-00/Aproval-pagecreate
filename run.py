try:
    import pagereg  # ye pageregproxy.cpython-312.so ko load karega
except ImportError as e:
    print("[ERROR] Compiled module nahi mila:", e)
    raise SystemExit

# Yahan pe tumhe wahi function call karna hai jo tumne pageregproxy.py me banaya tha.
try:
    pagereg.aprov()  # agar tumne main() function banaya hai
except AttributeError:
    print("[ERROR] pageregproxy.main() function nahi mila. Apna pageregproxy module check karo.")
