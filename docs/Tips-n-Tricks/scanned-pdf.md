# Make PDF Look Scanned
```
# use ImageMagick convert
# the order is important. the density argument applies to input.pdf and resize and rotate to output.pdf
convert -density 90 input.pdf -rotate 0.5 -attenuate 0.2 +noise Multiplicative -colorspace Gray output.pdf
```

Credits: https://gist.github.com/andyrbell/25c8632e15d17c83a54602f6acde2724
