
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ICONST CCONST SCONST COMMA PLUS MINUS TIMES DIVIDE COLON LPAREN RPAREN ASSIGN SEMI ARROW LTEQUAL LESS GREATER GTEQUAL EQUAL LBRACKET RBRACKET ID MODULO AND OR NOTEQ NOT DO DCL RETURN THEN INT FALSE CHARS SYN ELSE DOWN NUM RESULT IN FI ARRAY NULL LENGTH BY LOWER IF LOC CHAR REF END FOR READ PROC OD WHILE UPPER ASC TO RETURNS ABS EXIT ELSIF PRINT BOOL TYPE TRUEprogram : statement_liststatement_list : statement statement_nullablestatement_nullable : statement statement_nullable\n                              | emptystatement : declaration_statementdeclaration_statement : DCL declaration_list SEMIdeclaration_list : declaration\n                            | declaration COMMA declarationdeclaration : identifier_list modeidentifier_list : ID\n                           | ID COMMA identifier_listmode : discrete_modediscrete_mode : integer_mode\n                         | boolean_mode\n                         | character_modeinteger_mode : INTboolean_mode : BOOLcharacter_mode : CHARempty :'
    
_lr_action_items = {'DCL':([0,3,4,11,13,],[1,1,-5,1,-6,]),'SEMI':([6,7,15,16,17,18,19,20,21,22,25,],[13,-7,-16,-14,-15,-18,-13,-9,-12,-17,-8,]),'INT':([8,9,26,],[15,-10,-11,]),'CHAR':([8,9,26,],[18,-10,-11,]),'COMMA':([7,9,15,16,17,18,19,20,21,22,],[14,23,-16,-14,-15,-18,-13,-9,-12,-17,]),'BOOL':([8,9,26,],[22,-10,-11,]),'ID':([1,14,23,],[9,9,9,]),'$end':([2,3,4,5,10,11,12,13,24,],[0,-19,-5,-1,-2,-19,-4,-6,-3,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'statement_nullable':([3,11,],[10,24,]),'character_mode':([8,],[17,]),'declaration':([1,14,],[7,25,]),'boolean_mode':([8,],[16,]),'declaration_list':([1,],[6,]),'discrete_mode':([8,],[21,]),'program':([0,],[2,]),'integer_mode':([8,],[19,]),'mode':([8,],[20,]),'statement':([0,3,11,],[3,11,11,]),'declaration_statement':([0,3,11,],[4,4,4,]),'statement_list':([0,],[5,]),'identifier_list':([1,14,23,],[8,8,26,]),'empty':([3,11,],[12,12,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> statement_list','program',1,'p_program','Parser.py',13),
  ('statement_list -> statement statement_nullable','statement_list',2,'p_statement_list','Parser.py',17),
  ('statement_nullable -> statement statement_nullable','statement_nullable',2,'p_statement_nullable','Parser.py',21),
  ('statement_nullable -> empty','statement_nullable',1,'p_statement_nullable','Parser.py',22),
  ('statement -> declaration_statement','statement',1,'p_statement','Parser.py',32),
  ('declaration_statement -> DCL declaration_list SEMI','declaration_statement',3,'p_declaration_statement','Parser.py',37),
  ('declaration_list -> declaration','declaration_list',1,'p_declaration_list','Parser.py',41),
  ('declaration_list -> declaration COMMA declaration','declaration_list',3,'p_declaration_list','Parser.py',42),
  ('declaration -> identifier_list mode','declaration',2,'p_declaration','Parser.py',52),
  ('identifier_list -> ID','identifier_list',1,'p_identifier_list','Parser.py',56),
  ('identifier_list -> ID COMMA identifier_list','identifier_list',3,'p_identifier_list','Parser.py',57),
  ('mode -> discrete_mode','mode',1,'p_mode','Parser.py',74),
  ('discrete_mode -> integer_mode','discrete_mode',1,'p_discrete_mode','Parser.py',77),
  ('discrete_mode -> boolean_mode','discrete_mode',1,'p_discrete_mode','Parser.py',78),
  ('discrete_mode -> character_mode','discrete_mode',1,'p_discrete_mode','Parser.py',79),
  ('integer_mode -> INT','integer_mode',1,'p_integer_mode','Parser.py',83),
  ('boolean_mode -> BOOL','boolean_mode',1,'p_boolean_mode','Parser.py',86),
  ('character_mode -> CHAR','character_mode',1,'p_character_mode','Parser.py',89),
  ('empty -> <empty>','empty',0,'p_empty','Parser.py',94),
]
