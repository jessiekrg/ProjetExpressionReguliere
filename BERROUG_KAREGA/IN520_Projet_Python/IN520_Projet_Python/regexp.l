%{
#include "regexp.tab.h"   // <- utilise le header généré par Bison
extern YYSTYPE yylval;

%}

lettre [a-c]
sep [ \t]

%%

{sep} {}
\n          { return FIN_INSTRUCTION; }
"("          { return PAR_O; }
")"          { return PAR_F; }
"+"          { return PLUS; }
"*"          { return ETOILE; }
"."          { return POINT; }
{lettre}   { yylval.str = strdup(yytext); return LTR; }
"E"   { yylval.str = strdup("E"); return EPSILON; }
. {printf("Erreur : le robot ne connaît pas le symbole %s\n", yytext);}

%%


int yywrap() {
    return 1;
    }


