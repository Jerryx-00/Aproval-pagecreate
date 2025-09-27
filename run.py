#!/usr/bin/env python3
"""
run.py

Light wrapper to run your page tool in Termux or regular Python.
It will try to import a compiled extension (`page`), then fallback to `page.py`.
After loading it will call `main()` if present, otherwise `aprov()`.

Usage:
  python run.py

If you see ImportError, make sure your compiled .so or page.py is in the
same folder as this run.py.
"""
import os
import sys
import glob
import importlib
import importlib.util

SEARCH_ORDER = [
    "page",   # compiled module you mentioned earlier
]


def load_module():
    # try normal imports first
    for name in SEARCH_ORDER:
        try:
            return importlib.import_module(name)
        except Exception:
            pass

    # try files matching *.so (compiled extensions) that look like page
    for pattern in ("*.so", "*.cpython-*.so"):
        for path in glob.glob(os.path.join(os.getcwd(), pattern)):
            base = os.path.splitext(os.path.basename(path))[0]
            # try importing by base name
            try:
                return importlib.import_module(base)
            except Exception:
                # try loading by full path
                try:
                    spec = importlib.util.spec_from_file_location(base, path)
                    mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(mod)
                    return mod
                except Exception:
                    pass

    # finally try loading page.py directly
    page_py = os.path.join(os.getcwd(), "page.py")
    if os.path.isfile(page_py):
        spec = importlib.util.spec_from_file_location("page_local", page_py)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    raise ImportError("Could not find a module to load. Make sure 'page'/.so or 'page.py' exists in this folder.")


def main():
    mod = load_module()

    # prefer explicit main()
    if hasattr(mod, "main") and callable(mod.main):
        try:
            mod.main()
            return
        except Exception:
            # fallthrough to aprov
            pass

    # fallback to aprov()
    if hasattr(mod, "aprov") and callable(mod.aprov):
        mod.aprov()
        return

    print("Module loaded but no entrypoint 'main' or 'aprov' found.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted by user. Exiting.")
        sys.exit(1)
