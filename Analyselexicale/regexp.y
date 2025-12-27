%{
/* Librairies C standard */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Déclaration obligatoire pour Mac/Clang */
void yyerror(const char *s);  // pour éviter le warning
int yylex(void);               // déclaration de la fonction lexicale

/* Définition de yyerror */
void yyerror(const char *s) {
    fprintf(stderr, "Erreur syntaxe : %s\n", s);
}

/* yyparse() est généré par Bison */
%}

/* on déclare les tokens, les mêmes que Lex renvoie */
%token PAR_O
%token PAR_F
%token PLUS
%token ETOILE
%token POINT

%token <str> LTR EPSILON


/* on déclare l'associativité gauche avec %left, c'est à dire qu'on commence par le gauche pour regrouper les opérations */
/* on définit aussi les priorités des opérateurs, plus l'opérateur est bas dans le fichier et plus il est prioritaire */

%left PLUS POINT
%right ETOILE /* right car chaque étoile s'applique sur au plus proche élement à sa gauche*/

%union {
    char *str;
} /* définit le type de données que chaque token ou symbole non terminal peut transporter */

%type <str> expression plus_expression point_expression etoile_expression expression_primaire /* dit à Bison que ces non-terminaux utilisent le champ str de %union */ 
 

/* GRAMMAIRE */

%%

instruction: 
        expression 
        {
            /* $1 correspond à la valeur de l'expression (calculée par la règle 'expression'), ça peut être une lettre seule ou bien un combinaison */
            printf("= %s\n",$1);
        } 
    ;
expression: plus_expression;

/* UNION */
plus_expression: 
        plus_expression PLUS point_expression
        { 
            $$ = malloc(strlen($1)+strlen($3)+20);
            sprintf($$, "union(%s,%s)", $1, $3);
            free($1); free($3);
        }
    |   point_expression { $$ = $1; }
    ;

/* CONCATENATION */
point_expression:
        point_expression POINT etoile_expression
        {
            $$ = malloc(strlen($1)+strlen($3)+30);
            sprintf($$, "concatenation(%s,%s)", $1, $3);
            free($1); free($3);
        }
    |   point_expression etoile_expression
        {
            $$ = malloc(strlen($1)+strlen($2)+30);
            sprintf($$, "concatenation(%s,%s)", $1, $2);
            free($1); free($2);
        }
    |   etoile_expression { $$ = $1; }
    ;
/* ETOILE */
etoile_expression:
        expression_primaire ETOILE
        {
            $$ = malloc(strlen($1)+20);
            sprintf($$, "etoile(%s)", $1);
            free($1);
        }
    |   expression_primaire { $$ = $1; }
    ;

expression_primaire:
        PAR_O expression PAR_F  { $$ = $2; } /* on récupère simplement la valeur de l’expression interne */
    |   LTR 
        {
            $$ = malloc(strlen($1)+20);
            sprintf($$, "automate(\"%s\")", $1);
            free($1);
        }
    |   EPSILON { $$ = strdup("automate(\"E\")"); }
    ;
%%

int main() {
    yyparse();
    return 0;
}

