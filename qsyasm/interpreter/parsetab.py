
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftPLUSMINleftMULDIVleftPOWrightUMINADJ COMMA DIV FLOAT IDENT INTEGER LBRACKET LPAREN MIN MUL NEWLINE PLUS POW RBRACKET RPARENprogram : program instruction\n                   | instructioninstruction : normal_instruction\n                       | adjoint_instructionnormal_instruction : term argument_list\n                              | param_term argument_listadjoint_instruction : ADJ normal_instructioninstruction : NEWLINEterm : IDENT\n                | INTEGER\n                | lookuplookup : IDENT LBRACKET INTEGER RBRACKETparam_term : IDENT LPAREN expression RPARENargument_list : termargument_list : term COMMA argument_listexpression : expression PLUS expression\n                      | expression MIN expression\n                      | expression DIV expression\n                      | expression POW expression\n                      | expression MUL expressionexpression : LPAREN expression RPARENexpression : INTEGERexpression : FLOATexpression : MIN expression %prec UMINexpression : IDENT'
    
_lr_action_items = {'NEWLINE':([0,1,2,3,4,5,10,11,12,13,14,15,16,17,28,37,],[5,5,-2,-3,-4,-8,-10,-11,-1,-14,-5,-9,-6,-7,-15,-12,]),'ADJ':([0,1,2,3,4,5,10,11,12,13,14,15,16,17,28,37,],[8,8,-2,-3,-4,-8,-10,-11,-1,-14,-5,-9,-6,-7,-15,-12,]),'IDENT':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,20,22,24,28,30,31,32,33,34,35,37,],[9,9,-2,-3,-4,-8,15,15,9,-9,-10,-11,-1,-14,-5,-9,-6,-7,21,15,21,21,-15,-13,21,21,21,21,21,-12,]),'INTEGER':([0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,22,24,28,30,31,32,33,34,35,37,],[10,10,-2,-3,-4,-8,10,10,10,-9,-10,-11,-1,-14,-5,-9,-6,-7,25,27,10,25,25,-15,-13,25,25,25,25,25,-12,]),'$end':([1,2,3,4,5,10,11,12,13,14,15,16,17,28,37,],[0,-2,-3,-4,-8,-10,-11,-1,-14,-5,-9,-6,-7,-15,-12,]),'LPAREN':([9,18,22,24,31,32,33,34,35,],[18,22,22,22,22,22,22,22,22,]),'LBRACKET':([9,15,],[19,19,]),'COMMA':([10,11,13,15,37,],[-10,-11,20,-9,-12,]),'FLOAT':([18,22,24,31,32,33,34,35,],[26,26,26,26,26,26,26,26,]),'MIN':([18,21,22,23,24,25,26,29,31,32,33,34,35,36,38,39,40,41,42,43,],[24,-25,24,32,24,-22,-23,32,24,24,24,24,24,-24,-21,-16,-17,-18,-19,-20,]),'RPAREN':([21,23,25,26,29,36,38,39,40,41,42,43,],[-25,30,-22,-23,38,-24,-21,-16,-17,-18,-19,-20,]),'PLUS':([21,23,25,26,29,36,38,39,40,41,42,43,],[-25,31,-22,-23,31,-24,-21,-16,-17,-18,-19,-20,]),'DIV':([21,23,25,26,29,36,38,39,40,41,42,43,],[-25,33,-22,-23,33,-24,-21,33,33,-18,-19,-20,]),'POW':([21,23,25,26,29,36,38,39,40,41,42,43,],[-25,34,-22,-23,34,-24,-21,34,34,34,-19,34,]),'MUL':([21,23,25,26,29,36,38,39,40,41,42,43,],[-25,35,-22,-23,35,-24,-21,35,35,-18,-19,-20,]),'RBRACKET':([27,],[37,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'instruction':([0,1,],[2,12,]),'normal_instruction':([0,1,8,],[3,3,17,]),'adjoint_instruction':([0,1,],[4,4,]),'term':([0,1,6,7,8,20,],[6,6,13,13,6,13,]),'param_term':([0,1,8,],[7,7,7,]),'lookup':([0,1,6,7,8,20,],[11,11,11,11,11,11,]),'argument_list':([6,7,20,],[14,16,28,]),'expression':([18,22,24,31,32,33,34,35,],[23,29,36,39,40,41,42,43,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> program instruction','program',2,'p_program','parser.py',26),
  ('program -> instruction','program',1,'p_program','parser.py',27),
  ('instruction -> normal_instruction','instruction',1,'p_instruction','parser.py',40),
  ('instruction -> adjoint_instruction','instruction',1,'p_instruction','parser.py',41),
  ('normal_instruction -> term argument_list','normal_instruction',2,'p_normal_instruction','parser.py',45),
  ('normal_instruction -> param_term argument_list','normal_instruction',2,'p_normal_instruction','parser.py',46),
  ('adjoint_instruction -> ADJ normal_instruction','adjoint_instruction',2,'p_adjoint_instruction','parser.py',50),
  ('instruction -> NEWLINE','instruction',1,'p_instruction_newline','parser.py',61),
  ('term -> IDENT','term',1,'p_term','parser.py',65),
  ('term -> INTEGER','term',1,'p_term','parser.py',66),
  ('term -> lookup','term',1,'p_term','parser.py',67),
  ('lookup -> IDENT LBRACKET INTEGER RBRACKET','lookup',4,'p_lookup','parser.py',71),
  ('param_term -> IDENT LPAREN expression RPAREN','param_term',4,'p_param_term','parser.py',75),
  ('argument_list -> term','argument_list',1,'p_argument_list','parser.py',79),
  ('argument_list -> term COMMA argument_list','argument_list',3,'p_argument_list_args','parser.py',83),
  ('expression -> expression PLUS expression','expression',3,'p_expression_bin_op','parser.py',88),
  ('expression -> expression MIN expression','expression',3,'p_expression_bin_op','parser.py',89),
  ('expression -> expression DIV expression','expression',3,'p_expression_bin_op','parser.py',90),
  ('expression -> expression POW expression','expression',3,'p_expression_bin_op','parser.py',91),
  ('expression -> expression MUL expression','expression',3,'p_expression_bin_op','parser.py',92),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','parser.py',107),
  ('expression -> INTEGER','expression',1,'p_expression_integer','parser.py',111),
  ('expression -> FLOAT','expression',1,'p_expression_float','parser.py',115),
  ('expression -> MIN expression','expression',2,'p_expression_unary_min','parser.py',119),
  ('expression -> IDENT','expression',1,'p_expression_ident','parser.py',123),
]
