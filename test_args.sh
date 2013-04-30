if [ $@ ]
then
    first=$@
else
    echo Must be called with a path
    exit 0
fi

if [ ! -e $first ]
then
    echo Path doest not exist
    exit 0
fi

# mktemp -d $user-XXXXXXXXX --tmpdir
input_dir=$(mktemp -d)
cp $first/* $input_dir/


rm -rf $input_dir