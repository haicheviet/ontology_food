# -*- coding: utf-8 -*-
# Owlready
# Copyright (C) 2013-2017 Jean-Baptiste LAMY
# LIMICS (Laboratoire d'informatique médicale et d'ingénierie des connaissances en santé), UMR_S 1142
# University Paris 13, Sorbonne paris-Cité, Bobigny, France

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import sys, json
from collections import defaultdict
from urllib.parse import urljoin

try:
  from owlready2.base import OwlReadyOntologyParsingError
except:
  class OwlReadyOntologyParsingError(OwlReadyError): pass

  
"""

X ID
X LANGUAGE
X LIST
  SET
X TYPE
X VALUE
  INDEX
  BASE
X REVERSE

CONTEXT

VOCAB
GRAPH


"""

class Alias(object):
  def __init__(self, alias, name, type, container, reverse = False):
    self.alias     = alias
    self.name      = name
    self.type      = type
    self.reverse   = reverse
    self.container = container

class Container(object):
  def __init__(self, type, has_lang = False, has_index = False):
    self.type      = type
    self.has_lang  = has_lang
    self.has_index = has_index
    
class Context(object):
  def __init__(self, parent = None):
    self.parent = parent
    if parent:
      self.alias = dict(parent.alias)
      self.base  = parent.base
    else:
      self.alias = {}
      self.base  = ""
      
  def register(self, alias, name, type, containers, reverse = False):
    if containers:
      container = Container(None)
      if isinstance(containers, str): containers = [containers]
      for c in containers:
        if   self.is_keyword(c, "@language"): container.has_lang  = True
        elif self.is_keyword(c, "@index"):    container.has_index = True
        else:
          if c in self.alias: c = self.alias[c].name
          container.type = c
      container = Container(container)
    else:
      container = None
    self.alias[alias] = Alias(alias, name, type, container, reverse)
    if name.startswith("@"):
      if self.__class__ is Context:
        self.__class__ = AliasedKeywordContext
        self.keywords = {}
      if not name in self.keywords: keywords[name] = [name, alias]
      else:                         self.keywords[name].append(alias)
      
  def get_keyword(self, d, k): return d.get(k)
      
  def is_keyword(self, k, kref): return k == kref
  
  
class AliasedKeywordContext(Context):
  def __init__(self, parent = None):
    Context.__init__(self, parent)
    self.keywords = parent.copy()
    
  def get_keyword(self, d, k):
    for k2 in self.keywords[k]:
      r = d.get(k2)
      if not r is None: return r
  
  def is_keyword(self, k, kref):
    return k in self.keywords[kref]

  
  
def parse(f, on_triple = None, on_prepare_triple = None, new_blank = None, new_literal = None, default_base = ""):
  prefixes                 = {}
  prefixess                = [prefixes]
  tag_is_predicate         = False
  current_blank            = 0
  nb_triple                = 0
  bns                      = defaultdict(set)
  if default_base:
    xml_base = default_base
    if xml_base.endswith("#") or xml_base.endswith("/"): xml_base = xml_base[:-1]
    xml_dir  = xml_base.rsplit("/", 1)[0] + "/"
  else:
    xml_base                 = ""
    xml_dir                  = ""
    
  if not on_triple:
    def on_triple(s,p,o):
      print("%s %s %s ." % (s,p,o))
      
  if not on_prepare_triple:
    def on_prepare_triple(s,p,o):
      nonlocal nb_triple
      nb_triple += 1
      if not s.startswith("_"): s = "<%s>" % s
      if not (o.startswith("_") or o.startswith('"')): o = "<%s>" % o
      on_triple(s,"<%s>" % p,o)
      
  if not new_blank:
    def new_blank():
      nonlocal current_blank
      current_blank += 1
      return "_:%s" % current_blank
    
  node_2_blanks = defaultdict(new_blank)
  known_nodes   = set()
  
  if not new_literal:
    def new_literal(value, datatype = "", lang = ""):
      value = value.replace('"', '\\"').replace("\n", "\\n")
      if lang: return '"%s"@%s' % (value, lang)
      if datatype: return '"%s"^^<%s>' % (value, datatype)
      return '"%s"' % (value)
    
  if isinstance(f, str): ds = json.load(open(f))
  else:                  ds = json.load(f)
  
  
  def parse_node(d, context, in_context = False, no_literal = False):
    if isinstance(d, list):
      return [parse_node(i, context, in_context, no_literal) for i in d]
    if isinstance(d, str):
      if no_literal: return d
      if context.default_type:
        if context.default_type == "@id": return urljoin(context.base, d)
        return new_literal(d, context.default_type)
      else:
        return new_literal(d)
    w = context.get_keyword(d, "@value")
    if w:
      if context.default_type:
        if context.default_type == "@id": return d
        return new_literal(w, context.default_type, context.get_keyword(d, "@language"))
      else:
        return new_literal(w, context.get_keyword(d, "@type"), context.get_keyword(d, "@language"))
    w = context.get_keyword(d, "@list") or context.get_keyword(d, "@list")
    if w:
      return [parse_node(i, context, in_context, no_literal) for i in w]
    w = context.get_keyword(d, "@graph")
    if w:
      for d2 in w:
        parse_node(d2, context, in_context, no_literal)
    if "@context" in d:
      context = context.__class__(context)
      for k2, v2 in d["@context"].items():
        if context.is_keyword(k2, "@base"):
          context.base = v2
          continue
        if isinstance(v2, str):
          context.register(k2, v2, None, None)
        else:
          container = context.get_keyword(v2, "@container")
          w = context.get_keyword(v2, "@reverse")
          if w:
            context.register(k2, w, context.get_keyword(v2, "@type"), context.get_keyword(v2, "@container"), True)
          else:
            w = context.get_keyword(v2, "@id")
            if w:
              context.register(k2, w, context.get_keyword(v2, "@type"), context.get_keyword(v2, "@container"))
              
    name = context.get_keyword(d, "@id")
    if name:
      name = urljoin(context.base, name)
    else:
      name = new_blank()
    
    for k, v in d.items():
      if k in context.alias:
        alias = context.alias[k]
        context.default_type = alias.type
        k = alias.name
        reverse = alias.reverse
      else:
        context.default_type = None
        reverse = False
      if   context.is_keyword(k, "@reverse"):
        if in_context:
          pass
        else:
          for k2, v2 in v.items():
            v2 = parse_node(v2, context, in_context, no_literal)
            if not isinstance(v2, list): v2 = [v2]
            for v3 in v2:
              on_prepare_triple(v3, k2, name)
        continue
      elif context.is_keyword(k, "@type"):
        k = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
        v = parse_node(v, context, in_context, no_literal = True)
      elif k.startswith("@"):
        continue
      else:
        v = parse_node(v, context, in_context, no_literal)
        
      #print()
      #print(k, v)
      #print()

      if reverse:
        if isinstance(v, list):
          for v2 in v:
            on_prepare_triple(v2, k, name)
        else:
          on_prepare_triple(v, k, name)
      else:
        if isinstance(v, list):
          for v2 in v:
            on_prepare_triple(name, k, v2)
        else:
          on_prepare_triple(name, k, v)
        
    return name
  
  context = Context()
  if isinstance(ds, list):
    for d in ds:
      parse_node(d, context)
  else:
    parse_node(ds, context)
    
  return nb_triple


if __name__ == "__main__":
  filename = sys.argv[-1]
  
  import time
  t = time.time()
  nb_triple = parse(filename)
  t = time.time() - t
  print("# %s triples read in %ss" % (nb_triple, t), file = sys.stderr)
