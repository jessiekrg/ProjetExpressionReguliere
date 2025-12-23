%{
#include "tokens.h"
%}

lettre [a-c]
sep [ \t\n]

%%

{sep} {}
{lettre} {return LTR; }
"(" {return PAR_O;}
")" {return PAR_F;}
"+" {return PLUS;}
"*" {return ETOILE;}
"." {return POINT;}
"E" {return EPSILON;}

%%


int yywrap() {
    printf("fin de lecture du fichier ahahahaha \n");
    return 1;
    }





