LDFLAGS = -L/opt/homebrew/opt/flex/lib


all : idk_yet 

idk_yet : regexp.tab.c lex.yy.c
	gcc -o idk_yet regexp.tab.c lex.yy.c $(LDFLAGS) -lfl 

regexp.tab.c : regexp.y
	bison -d regexp.y

lex.yy.c : regexp.l
	flex regexp.l

clean:
	rm -f idk_yet regexp.tab.c regexp.tab.h lex.yy.c 

test : 
	echo "Test du fichier test"
	./idk_yet < test.1
	echo "Succès?"





#>bison -d regexp.y #bison creait notre pseudo dico de symboles là, il va creer regexp.tab.c
#>flex regexp.l  #flex lit le le dico ce qui creéait lex.yy.c
#>gcc -o idk_yet y.tab.c lex.yy.c -lfl 
#on compile nos fichiers c générés, 
#je met le -lfl car autrement le compilateur il reconnait pas les fonctions faites par lex car elles sont pas ds la bibilio ds les bibliothèque de l'ordi
