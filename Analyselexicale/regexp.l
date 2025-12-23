%{
#include "tokens.h"
%}

lettre [a-c]
sep [ \t\n]

%%

{sep} {}
{lettre} {printf("J'ai vu une lettre\n");return LTR; }
"(" {printf("J'ai vu une parenthèse\n");return PAR_O;}
")" {printf("J'ai vu une parenthèse\n");return PAR_F;}
"+" {printf("J'ai vu un +\n");return PLUS;}
"*" {printf("J'ai vu une etoile\n");return ETOILE;}
"." {printf("J'ai vu un point\n");return POINT;}
"E" {printf("J'ai vu une epsilon\n");return EPSILON;}
. {printf("Erreur : le robot ne connaît pas le symbole %s\n", yytext);}

%%


int yywrap() {
    printf("fin de lecture du fichier ahahahaha \n");
    return 1;
    }

int main() {
    while (yylex() != 0) ;
    return 0;}



