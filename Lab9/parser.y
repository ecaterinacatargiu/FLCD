%{
#include <stdio.h>
#include <stdlib.h>

#define YYDEBUG 1
%}

%token ID
%token CONST
%token start
%token end
%token if
%token else
%token while
%token for 
%token number 
%token boolean
%token string
%token read
%token print

%start program

%%

program : start declarationList stmt_list end ;
	declarationList : declaration ';' declarationList | declaration ;
declaration : type ID ';' ;
	    type : number | boolean | string ;
stmt_list : stmt ';' stmt_list | stmt ;
	  stmt : read_stmt | print_stmt | assign_stmt | if_stmt | while_stmt | for_stmt ;
read_stmt : read ID ;
	  print_stmt : print ID ;
assign_stmt : ID  '=' expression ;
	    expression : term | term '+' term | term '-' term | term '*' term | term '/' term | term '%' term ;
term : ID | CONST ;
if_stmt : if '(' condition ')' '{' stmt_list '}' else '{' stmt_list '}' | if '(' condition ')' '{' stmt_list '}' ;
	while_stmt : while '(' condition ')'  '{'  stmt_list '}' ;
for_stmt : for '(' assign_stmt ';' condition ';' expression ')' '{' stmt_list  '}' ;
	 condition : expression relation expression
relation : '<' | "<=" | "==" | ">=" | '>' ; 


%%

yyerror(char *s)
{
  printf("%s\n", s);
}

extern FILE *yyin;

main(int argc, char **argv)
{
  if (argc > 1) 
    yyin = fopen(argv[1], "r");
  if ( (argc > 2) && ( !strcmp(argv[2], "-d") ) ) 
    yydebug = 1;
  if ( !yyparse() ) 
    fprintf(stderr,"\t U GOOOOOD !!!\n");
}
