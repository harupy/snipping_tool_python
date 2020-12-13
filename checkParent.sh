git show-branch \
> | sed "s/].*//" \
> | grep "\*" \
> | grep -v "$(git rev-parse --abbrev-ref HEAD)" \
> | head -n1 \
> | sed "s/^.*\[//