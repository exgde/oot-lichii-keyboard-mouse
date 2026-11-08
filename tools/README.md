# Tools

They build the `ButtonPrompts-KeyboardMouse` folder from **your** OOT `.nup`.

```
pip install -r requirements.txt
python build_mod.py --nup "<your .nup>" --out output
```

Full guide, what each file does and how to redo the icons after changing the keys: [../docs/BUILD-THE-MOD.md](../docs/BUILD-THE-MOD.md).

Extracted files go to `tools/work/` and generated art to `tools/assets/`; both are in `.gitignore`.
