$ git add -p all_checks.py

diff --git a/all_checks.py b/all_checks.py
index 710266a..fdc4476 100644
--- a/all_checks.py
+++ b/all_checks.py
@@ -10,5 +10,8 @@ def main():
         print("Pending Reboot.")
         sys.exit(1)
 
+    print("Everything ok.")
+    sys.exit(0)
+
 main()
Stage this hunk [y,n,q,a,d,e,?]? y
# (ここで「y」を入力してEnterを押すと、この変更部分だけがコミット対象として追加されます)
