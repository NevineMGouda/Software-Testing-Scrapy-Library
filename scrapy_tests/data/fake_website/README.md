One can create many pages using, for example, `sed`:

```bash
for i in {1..15}
do
    cat template.html | sed -e "s,@TITLE@,$i," -e "s,@CONTENT@,$i," > $i.html
done
```

As a one-line command, as it might be useful:
```bash
for i in {1..15}; do cat template.html | sed -e "s,@TITLE@,$i," -e "s,@CONTENT@,$i," > $i.html; done
```