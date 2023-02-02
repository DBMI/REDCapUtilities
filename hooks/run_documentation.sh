sphinx-apidoc -f -o .\\docs\\source .\\src\\REDCapUtilities
sphinx-build -b html .\\docs\\source .\\docs\\build\\html
cd .\\docs\\build\\html
git add --all
git commit -m "Deploy updates." --no-verify
git push -u origin gh-pages
