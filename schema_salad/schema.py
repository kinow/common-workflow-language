import avro
import copy
from .add_dictlist import add_dictlist
import sys
import pprint
from pkg_resources import resource_stream
import ruamel.yaml as yaml
import avro.schema
from . import validate
import json
import urlparse
import os
AvroSchemaFromJSONData = avro.schema.make_avsc_object
# AvroSchemaFromJSONData=avro.schema.SchemaFromJSONData
from avro.schema import Names, SchemaParseException
from . import ref_resolver
from .ref_resolver import Loader, DocumentType
from .flatten import flatten
import logging
from .aslist import aslist
from . import jsonld_context
from .sourceline import SourceLine, strip_dup_lineno, add_lc_filename, bullets, relname
from typing import Any, AnyStr, cast, Dict, List, Tuple, TypeVar, Union
from ruamel.yaml.comments import CommentedSeq, CommentedMap

_logger = logging.getLogger("salad")

salad_files = ('metaschema.yml',
               'metaschema_base.yml',
               'salad.md',
               'field_name.yml',
               'import_include.md',
               'link_res.yml',
               'ident_res.yml',
               'vocab_res.yml',
               'vocab_res.yml',
               'field_name_schema.yml',
               'field_name_src.yml',
               'field_name_proc.yml',
               'ident_res_schema.yml',
               'ident_res_src.yml',
               'ident_res_proc.yml',
               'link_res_schema.yml',
               'link_res_src.yml',
               'link_res_proc.yml',
               'vocab_res_schema.yml',
               'vocab_res_src.yml',
               'vocab_res_proc.yml')


def get_metaschema():
    # type: () -> Tuple[Names, List[Dict[unicode, Any]], Loader]
    loader = ref_resolver.Loader({
        "Any": "https://w3id.org/cwl/salad#Any",
        "ArraySchema": "https://w3id.org/cwl/salad#ArraySchema",
        "DocType": "https://w3id.org/cwl/salad#DocType",
        "Documentation": "https://w3id.org/cwl/salad#Documentation",
        "EnumSchema": "https://w3id.org/cwl/salad#EnumSchema",
        "JsonldPredicate": "https://w3id.org/cwl/salad#JsonldPredicate",
        "NamedType": "https://w3id.org/cwl/salad#NamedType",
        "RecordField": "https://w3id.org/cwl/salad#RecordField",
        "RecordSchema": "https://w3id.org/cwl/salad#RecordSchema",
        "SaladEnumSchema": "https://w3id.org/cwl/salad#SaladEnumSchema",
        "SaladRecordField": "https://w3id.org/cwl/salad#SaladRecordField",
        "SaladRecordSchema": "https://w3id.org/cwl/salad#SaladRecordSchema",
        "SchemaDefinedType": "https://w3id.org/cwl/salad#SchemaDefinedType",
        "SpecializeDef": "https://w3id.org/cwl/salad#SpecializeDef",
        "_container": "https://w3id.org/cwl/salad#JsonldPredicate/_container",
        "_id": {
            "@id": "https://w3id.org/cwl/salad#_id",
            "@type": "@id",
            "identity": True
        },
        "_type": "https://w3id.org/cwl/salad#JsonldPredicate/_type",
        "abstract": "https://w3id.org/cwl/salad#SaladRecordSchema/abstract",
        "array": "https://w3id.org/cwl/salad#array",
        "boolean": "http://www.w3.org/2001/XMLSchema#boolean",
        "dct": "http://purl.org/dc/terms/",
        "doc": "sld:doc",
        "docAfter": {
            "@id": "https://w3id.org/cwl/salad#docAfter",
            "@type": "@id"
        },
        "docChild": {
            "@id": "https://w3id.org/cwl/salad#docChild",
            "@type": "@id"
        },
        "docParent": {
            "@id": "https://w3id.org/cwl/salad#docParent",
            "@type": "@id"
        },
        "documentRoot": "https://w3id.org/cwl/salad#SchemaDefinedType/documentRoot",
        "documentation": "https://w3id.org/cwl/salad#documentation",
        "double": "http://www.w3.org/2001/XMLSchema#double",
        "enum": "https://w3id.org/cwl/salad#enum",
        "extends": {
            "@id": "https://w3id.org/cwl/salad#extends",
            "@type": "@id",
            "refScope": 1
        },
        "fields": {
            "@id": "https://w3id.org/cwl/salad#fields",
            "mapPredicate": "type",
            "mapSubject": "name"
        },
        "float": "http://www.w3.org/2001/XMLSchema#float",
        "identity": "https://w3id.org/cwl/salad#JsonldPredicate/identity",
        "int": "http://www.w3.org/2001/XMLSchema#int",
        "items": {
            "@id": "https://w3id.org/cwl/salad#items",
            "@type": "@vocab",
            "refScope": 2
        },
        "jsonldPredicate": "sld:jsonldPredicate",
        "long": "http://www.w3.org/2001/XMLSchema#long",
        "mapPredicate": "https://w3id.org/cwl/salad#JsonldPredicate/mapPredicate",
        "mapSubject": "https://w3id.org/cwl/salad#JsonldPredicate/mapSubject",
        "name": "@id",
        "noLinkCheck": "https://w3id.org/cwl/salad#JsonldPredicate/noLinkCheck",
        "null": "https://w3id.org/cwl/salad#null",
        "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
        "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
        "record": "https://w3id.org/cwl/salad#record",
        "refScope": "https://w3id.org/cwl/salad#JsonldPredicate/refScope",
        "sld": "https://w3id.org/cwl/salad#",
        "specialize": {
            "@id": "https://w3id.org/cwl/salad#specialize",
            "mapPredicate": "specializeTo",
            "mapSubject": "specializeFrom"
        },
        "specializeFrom": {
            "@id": "https://w3id.org/cwl/salad#specializeFrom",
            "@type": "@id",
            "refScope": 1
        },
        "specializeTo": {
            "@id": "https://w3id.org/cwl/salad#specializeTo",
            "@type": "@id",
            "refScope": 1
        },
        "string": "http://www.w3.org/2001/XMLSchema#string",
        "symbols": {
            "@id": "https://w3id.org/cwl/salad#symbols",
            "@type": "@id",
            "identity": True
        },
        "type": {
            "@id": "https://w3id.org/cwl/salad#type",
            "@type": "@vocab",
            "refScope": 2,
            "typeDSL": True
        },
        "typeDSL": "https://w3id.org/cwl/salad#JsonldPredicate/typeDSL",
        "xsd": "http://www.w3.org/2001/XMLSchema#"
    })

    for f in salad_files:
        rs = resource_stream(__name__, 'metaschema/' + f)
        loader.cache["https://w3id.org/cwl/" + f] = rs.read()
        rs.close()

    rs = resource_stream(__name__, 'metaschema/metaschema.yml')
    loader.cache["https://w3id.org/cwl/salad"] = rs.read()
    rs.close()

    j = yaml.round_trip_load(loader.cache["https://w3id.org/cwl/salad"])  # type: ignore
    add_lc_filename(j, "metaschema.yml")
    j, _ = loader.resolve_all(j, "https://w3id.org/cwl/salad#")

    # pprint.pprint(j)

    (sch_names, sch_obj) = make_avro_schema(j, loader)
    if isinstance(sch_names, Exception):
        _logger.error("Metaschema error, avro was:\n%s",
                      json.dumps(sch_obj, indent=4))
        raise sch_names
    validate_doc(sch_names, j, loader, strict=True)
    return (sch_names, j, loader)


def load_schema(schema_ref,  # type: Union[CommentedMap, CommentedSeq, unicode]
                cache=None   # type: Dict
                ):
    # type: (...) -> Tuple[Loader, Union[Names, SchemaParseException], Dict[unicode, Any], Loader]
    """Load a schema that can be used to validate documents using load_and_validate.

    return document_loader, avsc_names, schema_metadata, metaschema_loader"""

    metaschema_names, metaschema_doc, metaschema_loader = get_metaschema()
    if cache is not None:
        metaschema_loader.cache.update(cache)
    schema_doc, schema_metadata = metaschema_loader.resolve_ref(schema_ref, "")

    if not isinstance(schema_doc, list):
        raise ValueError("Schema reference must resolve to a list.")

    validate_doc(metaschema_names, schema_doc, metaschema_loader, True)
    metactx = schema_metadata.get("@context", {})
    metactx.update(schema_metadata.get("$namespaces", {}))
    (schema_ctx, rdfs) = jsonld_context.salad_to_jsonld_context(
        schema_doc, metactx)

    # Create the loader that will be used to load the target document.
    document_loader = Loader(schema_ctx, cache=cache)

    # Make the Avro validation that will be used to validate the target
    # document
    (avsc_names, avsc_obj) = make_avro_schema(schema_doc, document_loader)

    return document_loader, avsc_names, schema_metadata, metaschema_loader


def load_and_validate(document_loader,  # type: Loader
                      avsc_names,       # type: Names
                      document,         # type: Union[CommentedMap, unicode]
                      strict            # type: bool
                      ):
    # type: (...) -> Tuple[Any, Dict[unicode, Any]]
    """Load a document and validate it with the provided schema.

    return data, metadata
    """
    try:
        if isinstance(document, CommentedMap):
            source = document["id"]
            data, metadata = document_loader.resolve_all(
                document, document["id"], checklinks=False)
        else:
            source = document
            data, metadata = document_loader.resolve_ref(
                document, checklinks=False)
    except validate.ValidationException as v:
        raise validate.ValidationException(strip_dup_lineno(str(v)))

    validationErrors = u""
    try:
        document_loader.validate_links(data, u"")
    except validate.ValidationException as v:
        validationErrors = unicode(v) + "\n"

    try:
        validate_doc(avsc_names, data, document_loader, strict, source=source)
    except validate.ValidationException as v:
        validationErrors += unicode(v)

    if validationErrors:
        raise validate.ValidationException(validationErrors)

    return data, metadata


def validate_doc(schema_names,  # type: Names
                 doc,           # type: Union[Dict[unicode, Any], List[Dict[unicode, Any]], unicode]
                 loader,        # type: Loader
                 strict,        # type: bool
                 source=None
                 ):
    # type: (...) -> None
    has_root = False
    for r in schema_names.names.values():
        if ((hasattr(r, 'get_prop') and r.get_prop(u"documentRoot")) or (
                u"documentRoot" in r.props)):
            has_root = True
            break

    if not has_root:
        raise validate.ValidationException(
            "No document roots defined in the schema")

    if isinstance(doc, list):
        validate_doc = doc
    elif isinstance(doc, CommentedMap):
        validate_doc = CommentedSeq([doc])
        validate_doc.lc.add_kv_line_col(0, [doc.lc.line, doc.lc.col])
        validate_doc.lc.filename = doc.lc.filename
    else:
        raise validate.ValidationException("Document must be dict or list")

    roots = []
    for r in schema_names.names.values():
        if ((hasattr(r, "get_prop") and r.get_prop(u"documentRoot")) or (
                r.props.get(u"documentRoot"))):
            roots.append(r)

    anyerrors = []
    for pos, item in enumerate(validate_doc):
        sl = SourceLine(validate_doc, pos, unicode)
        success = False
        for r in roots:
            success = validate.validate_ex(
                r, item, loader.identifiers, strict,
                foreign_properties=loader.foreign_properties, raise_ex=False)
            if success:
                break

        if not success:
            errors = []  # type: List[unicode]
            for r in roots:
                if hasattr(r, "get_prop"):
                    name = r.get_prop(u"name")
                elif hasattr(r, "name"):
                    name = r.name

                try:
                    validate.validate_ex(
                        r, item, loader.identifiers, strict,
                        foreign_properties=loader.foreign_properties,
                        raise_ex=True)
                except validate.ClassValidationException as e:
                    errors = [sl.makeError(u"tried `%s` but\n%s" % (
                        name, validate.indent(str(e), nolead=False)))]
                    break
                except validate.ValidationException as e:
                    errors.append(sl.makeError(u"tried `%s` but\n%s" % (
                        name, validate.indent(str(e), nolead=False))))

            objerr = sl.makeError(u"Invalid")
            for ident in loader.identifiers:
                if ident in item:
                    objerr = sl.makeError(
                        u"Object `%s` is not valid because"
                        % (relname(item[ident])))
                    break
            anyerrors.append(u"%s\n%s" %
                             (objerr, validate.indent(bullets(errors, "- "))))
    if anyerrors:
        raise validate.ValidationException(
            strip_dup_lineno(bullets(anyerrors, "* ")))


def replace_type(items, spec, loader, found):
    # type: (Any, Dict[unicode, Any], Loader, Set[unicode]) -> Any
    """ Go through and replace types in the 'spec' mapping"""

    if isinstance(items, dict):
        # recursively check these fields for types to replace
        if "type" in items and items["type"] in ("record", "enum"):
            if items.get("name"):
                if items["name"] in found:
                    return items["name"]
                else:
                    found.add(items["name"])

        items = copy.copy(items)
        for n in ("type", "items", "fields"):
            if n in items:
                items[n] = replace_type(items[n], spec, loader, found)
                if isinstance(items[n], list):
                    items[n] = flatten(items[n])

        return items
    elif isinstance(items, list):
        # recursively transform list
        return [replace_type(i, spec, loader, found) for i in items]
    elif isinstance(items, (str, unicode)):
        # found a string which is a symbol corresponding to a type.
        replace_with = None
        if items in loader.vocab:
            # If it's a vocabulary term, first expand it to its fully qualified
            # URI
            items = loader.vocab[items]

        if items in spec:
            # Look up in specialization map
            replace_with = spec[items]

        if replace_with:
            return replace_type(replace_with, spec, loader, found)
    return items


def avro_name(url):  # type: (AnyStr) -> AnyStr
    doc_url, frg = urlparse.urldefrag(url)
    if frg:
        if '/' in frg:
            return frg[frg.rindex('/') + 1:]
        else:
            return frg
    return url


Avro = TypeVar('Avro', Dict[unicode, Any], List[Any], unicode)


def make_valid_avro(items,          # type: Avro
                    alltypes,       # type: Dict[unicode, Dict[unicode, Any]]
                    found,          # type: Set[unicode]
                    union=False     # type: bool
                    ):
    # type: (...) -> Union[Avro, Dict]
    if isinstance(items, dict):
        items = copy.copy(items)
        if items.get("name"):
            items["name"] = avro_name(items["name"])

        if "type" in items and items["type"] in ("https://w3id.org/cwl/salad#record", "https://w3id.org/cwl/salad#enum", "record", "enum"):
            if (hasattr(items, "get") and items.get("abstract")) or ("abstract"
                                                                     in items):
                return items
            if not items.get("name"):
                raise Exception(
                    "Named schemas must have a non-empty name: %s" % items)

            if items["name"] in found:
                return items["name"]
            else:
                found.add(items["name"])
        for n in ("type", "items", "values", "fields"):
            if n in items:
                items[n] = make_valid_avro(
                    items[n], alltypes, found, union=True)
        if "symbols" in items:
            items["symbols"] = [avro_name(sym) for sym in items["symbols"]]
        return items
    if isinstance(items, list):
        ret = []
        for i in items:
            ret.append(make_valid_avro(i, alltypes, found, union=union))
        return ret
    if union and isinstance(items, (str, unicode)):
        if items in alltypes and avro_name(items) not in found:
            return cast(Dict, make_valid_avro(alltypes[items], alltypes, found,
                                              union=union))
        items = avro_name(items)
    return items

def deepcopy_strip(item):  # type: (Any) -> Any
    """Make a deep copy of list and dict objects.

    Intentionally do not copy attributes.  This is to discard CommentedMap and
    CommentedSeq metadata which is very expensive with regular copy.deepcopy.

    """

    if isinstance(item, dict):
        return {k: deepcopy_strip(v) for k,v in item.iteritems()}
    elif isinstance(item, list):
        return [deepcopy_strip(k) for k in item]
    else:
        return item

def extend_and_specialize(items, loader):
    # type: (List[Dict[unicode, Any]], Loader) -> List[Dict[unicode, Any]]
    """Apply 'extend' and 'specialize' to fully materialize derived record
    types."""

    items = deepcopy_strip(items)
    types = {t["name"]: t for t in items}  # type: Dict[unicode, Any]
    n = []

    for t in items:
        if "extends" in t:
            spec = {}  # type: Dict[unicode, unicode]
            if "specialize" in t:
                for sp in aslist(t["specialize"]):
                    spec[sp["specializeFrom"]] = sp["specializeTo"]

            exfields = []  # type: List[unicode]
            exsym = []  # type: List[unicode]
            for ex in aslist(t["extends"]):
                if ex not in types:
                    raise Exception("Extends %s in %s refers to invalid base type" % (
                        t["extends"], t["name"]))

                basetype = copy.copy(types[ex])

                if t["type"] == "record":
                    if spec:
                        basetype["fields"] = replace_type(
                            basetype.get("fields", []), spec, loader, set())

                    for f in basetype.get("fields", []):
                        if "inherited_from" not in f:
                            f["inherited_from"] = ex

                    exfields.extend(basetype.get("fields", []))
                elif t["type"] == "enum":
                    exsym.extend(basetype.get("symbols", []))

            if t["type"] == "record":
                t = copy.copy(t)
                exfields.extend(t.get("fields", []))
                t["fields"] = exfields

                fieldnames = set()  # type: Set[unicode]
                for field in t["fields"]:
                    if field["name"] in fieldnames:
                        raise validate.ValidationException(
                            "Field name %s appears twice in %s" % (field["name"], t["name"]))
                    else:
                        fieldnames.add(field["name"])
            elif t["type"] == "enum":
                t = copy.copy(t)
                exsym.extend(t.get("symbols", []))
                t["symbol"] = exsym

            types[t["name"]] = t

        n.append(t)

    ex_types = {}
    for t in n:
        ex_types[t["name"]] = t

    extended_by = {}  # type: Dict[unicode, unicode]
    for t in n:
        if "extends" in t:
            for ex in aslist(t["extends"]):
                if ex_types[ex].get("abstract"):
                    add_dictlist(extended_by, ex, ex_types[t["name"]])
                    add_dictlist(extended_by, avro_name(ex), ex_types[ex])

    for t in n:
        if t.get("abstract") and t["name"] not in extended_by:
            raise validate.ValidationException(
                "%s is abstract but missing a concrete subtype" % t["name"])

    for t in n:
        if "fields" in t:
            t["fields"] = replace_type(t["fields"], extended_by, loader, set())

    return n

def make_avro_schema(i,         # type: List[Dict[unicode, Any]]
                     loader     # type: Loader
                     ):
    # type: (...) -> Tuple[Union[Names, SchemaParseException], List[Dict[unicode, Any]]]
    names = avro.schema.Names()

    j = extend_and_specialize(i, loader)

    name_dict = {}  # type: Dict[unicode, Dict[unicode, Any]]
    for t in j:
        name_dict[t["name"]] = t
    j2 = make_valid_avro(j, name_dict, set())

    j3 = [t for t in j2 if isinstance(t, dict) and not t.get(
        "abstract") and t.get("type") != "documentation"]

    try:
        AvroSchemaFromJSONData(j3, names)
    except avro.schema.SchemaParseException as e:
        return (e, j3)

    return (names, j3)
