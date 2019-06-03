.PHONY: all clean

clean:
	rm -rf ./lib/*.pyc
	rm -rf ./data/output/*
	rm -rf ./figure/*
#	rm -rf ./data/res/*
#	rm -rf ./data/input/*
	
push: clean
	git add --all
	git commit -m "${COMM}"
	git push origin master
