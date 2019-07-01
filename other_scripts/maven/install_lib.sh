f=$(basename $1)
name=$(echo $f | cut -d'.' -f1)

echo mvn install:install-file \
-Dfile=$1 \
-DgroupId=$name \
-DartifactId=$name \
-Dversion=1.0 \
-Dpackaging=jar

