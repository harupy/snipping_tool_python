# Automatically finds the current working branch
pushedrev=$(git branch | sed -n -e 's/^\* \(.*\)/\1/p')
echo "The current working branch is : '$pushedrev'"

basename=develop
if ! baserev="$(git rev-parse --verify refs/heads/"$basename" 2>/dev/null)"; then
    echo "'$basename' is missing, call for help!"
    exit 1
fi
parents_of_children_of_base="$(
  git rev-list --pretty=tformat:%P "$pushedrev" --not "$baserev" |
  grep -F "$baserev"
)"
case ",$parents_of_children_of_base" in
    ,)     echo "Must descend from tip of '$basename'"
           exit 1 ;;
    ,*\ *) echo "Must not merge tip of '$basename' (Please rebase instead)"
           exit 1 ;;
    ,*)    exit 0 ;;
esac