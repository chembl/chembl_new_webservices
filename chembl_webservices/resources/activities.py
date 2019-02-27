__author__ = 'mnowotka'

from tastypie import fields
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from chembl_webservices.core.resource import ChemblModelResource
from chembl_webservices.core.meta import ChemblResourceMeta
from chembl_webservices.core.serialization import ChEMBLApiSerializer
from chembl_webservices.core.utils import NUMBER_FILTERS, CHAR_FILTERS, FLAG_FILTERS
from django.db.models import Prefetch
from django.conf.urls import url
from tastypie.utils import trailing_slash

try:
    from chembl_compatibility.models import Activities
except ImportError:
    from chembl_core_model.models import Activities
try:
    from chembl_compatibility.models import ActivityProperties
except ImportError:
    from chembl_core_model.models import ActivityProperties
try:
    from chembl_compatibility.models import ActivitySupp
except ImportError:
    from chembl_core_model.models import ActivitySupp
try:
    from chembl_compatibility.models import ActivitySmid
except ImportError:
    from chembl_core_model.models import ActivitySmid
try:
    from chembl_compatibility.models import ActivitySuppMap
except ImportError:
    from chembl_core_model.models import ActivitySuppMap
try:
    from chembl_compatibility.models import Assays
except ImportError:
    from chembl_core_model.models import Assays
try:
    from chembl_compatibility.models import AssayType
except ImportError:
    from chembl_core_model.models import AssayType
try:
    from chembl_compatibility.models import BioassayOntology
except ImportError:
    from chembl_core_model.models import BioassayOntology
try:
    from chembl_compatibility.models import ChemblIdLookup
except ImportError:
    from chembl_core_model.models import ChemblIdLookup
try:
    from chembl_compatibility.models import CompoundRecords
except ImportError:
    from chembl_core_model.models import CompoundRecords
try:
    from chembl_compatibility.models import CompoundStructures
except ImportError:
    from chembl_core_model.models import CompoundStructures
try:
    from chembl_compatibility.models import DataValidityLookup
except ImportError:
    from chembl_core_model.models import DataValidityLookup
try:
    from chembl_compatibility.models import Docs
except ImportError:
    from chembl_core_model.models import Docs
try:
    from chembl_compatibility.models import MoleculeDictionary
except ImportError:
    from chembl_core_model.models import MoleculeDictionary
try:
    from chembl_compatibility.models import TargetDictionary
except ImportError:
    from chembl_core_model.models import TargetDictionary
try:
    from chembl_compatibility.models import Source
except ImportError:
    from chembl_core_model.models import Source
try:
    from chembl_compatibility.models import LigandEff
except ImportError:
    from chembl_core_model.models import LigandEff


from chembl_webservices.core.fields import monkeypatch_tastypie_field
monkeypatch_tastypie_field()

# ----------------------------------------------------------------------------------------------------------------------


class LigandEfficiencyResource(ChemblModelResource):

    class Meta(ChemblResourceMeta):
        queryset = LigandEff.objects.all()
        resource_name = 'ligand_efficiency'
        collection_name = 'ligand_efficiencies'
        serializer = ChEMBLApiSerializer(resource_name, {collection_name: resource_name})
        filtering = {
            'bei': NUMBER_FILTERS,
            'sei': NUMBER_FILTERS,
            'le': NUMBER_FILTERS,
            'lle': NUMBER_FILTERS,
        }
        ordering = filtering.keys()


# ----------------------------------------------------------------------------------------------------------------------


class ActivityPropertiesResource(ChemblModelResource):
    class Meta(ChemblResourceMeta):
        queryset = ActivityProperties.objects.all()
        resource_name = 'activity_properties'
        collection_name = 'activity_properties'
        serializer = ChEMBLApiSerializer(resource_name, {collection_name: resource_name})

        filtering = {
            'type': CHAR_FILTERS,
            'relation': CHAR_FILTERS,
            'value': NUMBER_FILTERS,
            'units': CHAR_FILTERS,
            'text_value': CHAR_FILTERS,
            'standard_type': CHAR_FILTERS,
            'standard_relation': CHAR_FILTERS,
            'standard_value': NUMBER_FILTERS,
            'standard_units': CHAR_FILTERS,
            'standard_text_value': CHAR_FILTERS,
            'comments': CHAR_FILTERS,
            'result_flag': CHAR_FILTERS,
        }
        ordering = filtering.keys()

        fields = (
            'type',
            'relation',
            'value',
            'units',
            'text_value',
            'standard_type',
            'standard_relation',
            'standard_value',
            'standard_units',
            'standard_text_value',
            'comments',
            'result_flag',
        )


class ActivityResource(ChemblModelResource):

    bao_format = fields.CharField('assay__bao_format_id', null=True, blank=True)
    bao_label = fields.CharField('assay__bao_format__label', null=True, blank=True)
    bao_endpoint = fields.CharField('bao_endpoint_id', null=True, blank=True)
    data_validity_description = fields.CharField('data_validity_comment__description', null=True, blank=True)
    data_validity_comment = fields.CharField('data_validity_comment__data_validity_comment', null=True, blank=True)
    document_chembl_id = fields.CharField('doc__chembl_id', null=True, blank=True)
    molecule_chembl_id = fields.CharField('molecule__chembl_id', null=True, blank=True)
    molecule_pref_name = fields.CharField('molecule__pref_name', null=True, blank=True)
    parent_molecule_chembl_id = fields.CharField('molecule__moleculehierarchy__parent_molecule__chembl_id', null=True, blank=True)
    target_chembl_id = fields.CharField('assay__target__chembl_id', null=True, blank=True)
    target_pref_name = fields.CharField('assay__target__pref_name', null=True, blank=True)
    target_organism = fields.CharField('assay__target__organism', null=True, blank=True)
    target_tax_id = fields.CharField('assay__target__tax_id', null=True, blank=True)
    assay_chembl_id = fields.CharField('assay__chembl_id', null=True, blank=True)
    assay_type = fields.CharField('assay__assay_type__assay_type', null=True, blank=True)
    src_id = fields.IntegerField('src_id', null=True, blank=True)
    assay_description = fields.CharField('assay__description', null=True, blank=True)
    document_year = fields.IntegerField('doc__year', null=True, blank=True)
    document_journal = fields.CharField('doc__journal', null=True, blank=True)
    record_id = fields.IntegerField('record_id', null=True, blank=True)
    canonical_smiles = fields.CharField('molecule__compoundstructures__canonical_smiles', null=True, blank=True)
    ligand_efficiency = fields.ForeignKey('chembl_webservices.resources.activities.LigandEfficiencyResource',
                                            'ligandeff', full=True, null=True, blank=True)
    activity_properties = fields.ToManyField('chembl_webservices.resources.activities.ActivityPropertiesResource', 'activityproperties_set', full=True, null=True, blank=True)

    class Meta(ChemblResourceMeta):
        queryset = Activities.objects.all()
        resource_name = 'activity'
        collection_name = 'activities'
        serializer = ChEMBLApiSerializer(resource_name, {collection_name: resource_name, 'activity_properties': 'activity_properties'})
        prefetch_related = [
                            Prefetch('assay', queryset=Assays.objects.only('description', 'chembl', 'assay_id',
                                                                           'target', 'assay_type',
                                                                           'bao_format')),
                            Prefetch('assay__assay_type', queryset=AssayType.objects.only('assay_type', 'assay_desc')),
                            Prefetch('assay__bao_format', queryset=BioassayOntology.objects.only('bao_id', 'label')),
                            Prefetch('assay__target', queryset=TargetDictionary.objects.only('pref_name', 'chembl',
                                                                                             'organism', 'tid',
                                                                                             'tax_id')),
                            Prefetch('doc', queryset=Docs.objects.only('year', 'journal', 'chembl')),
                            Prefetch('ligandeff'),
                            Prefetch('molecule', queryset=MoleculeDictionary.objects.only('chembl')),
                            Prefetch('molecule__compoundstructures',
                                     queryset=CompoundStructures.objects.only('canonical_smiles')),
                            Prefetch('molecule__moleculehierarchy'),
                            Prefetch('molecule__moleculehierarchy__parent_molecule',
                                     queryset=MoleculeDictionary.objects.only('chembl')),
                            Prefetch('data_validity_comment',
                                     queryset=DataValidityLookup.objects.only('description', 'data_validity_comment')),
                            Prefetch('activityproperties_set'),
                            ]
        fields = (
            'activity_comment',
            'activity_id',
            'assay_chembl_id',
            'assay_description',
            'assay_type',
            'src_id',
            'bao_endpoint',
            'bao_format'
            'canonical_smiles',
            'data_validity_comment',
            'document_journal',
            'document_year',
            'document_chembl_id',
            'molecule_chembl_id',
            'molecule_pref_name',
            'parent_molecule_chembl_id',
            'pchembl_value',
            'potential_duplicate',
            'qudt_units',
            'record_id',
            'relation',
            'standard_flag',
            'standard_relation',
            'standard_text_value',
            'standard_type',
            'standard_units',
            'standard_upper_value',
            'standard_value',
            'target_pref_name',
            'target_organism',
            'text_value',
            'toid',
            'type',
            'units',
            'uo_units',
            'upper_value',
            'value',
        )
        filtering = {
            'activity_properties': ALL_WITH_RELATIONS,
            'activity_comment': CHAR_FILTERS,
            'activity_id': NUMBER_FILTERS,
            'assay_chembl_id': ALL,
            'assay_description': CHAR_FILTERS,
            'assay_type': CHAR_FILTERS,
            'bao_endpoint': ALL,
            'target_chembl_id': CHAR_FILTERS,
            'canonical_smiles': FLAG_FILTERS,
            'data_validity_comment': ALL,
            'document_chembl_id': ALL,
            'document_journal': CHAR_FILTERS,
            'document_year': NUMBER_FILTERS,
            'molecule_chembl_id': ALL,
            'molecule_pref_name': CHAR_FILTERS,
            'parent_molecule_chembl_id': ALL,
            'pchembl_value': NUMBER_FILTERS,
            'potential_duplicate': FLAG_FILTERS,
            'qudt_units': CHAR_FILTERS,
            'record_id': NUMBER_FILTERS,
            'relation': CHAR_FILTERS,
            'standard_flag': FLAG_FILTERS,
            'standard_relation': CHAR_FILTERS,
            'standard_text_value': CHAR_FILTERS,
            'standard_type': CHAR_FILTERS,
            'standard_units': CHAR_FILTERS,
            'standard_upper_value': NUMBER_FILTERS,
            'standard_value': NUMBER_FILTERS,
            'target_pref_name': CHAR_FILTERS,
            'target_organism': CHAR_FILTERS,
            'target_tax_id': NUMBER_FILTERS,
            'text_value': CHAR_FILTERS,
            'type': CHAR_FILTERS,
            'units': CHAR_FILTERS,
            'uo_units': CHAR_FILTERS,
            'upper_value': NUMBER_FILTERS,
            'value': NUMBER_FILTERS,
            'ligand_efficiency': ALL_WITH_RELATIONS,
        }
        ordering = [field for field in filtering.keys() if not ('comment' in field or 'description' in field or
                                                                'canonical_smiles' in field)]

    def prepend_urls(self):
        """
        Returns a URL scheme based on the default scheme to specify
        the response format as a file extension, e.g. /api/v1/users.json
        """
        return [
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_search'), name="api_get_search"),
            url(r"^(?P<resource_name>%s)/search\.(?P<format>xml|json|jsonp|yaml)$" % self._meta.resource_name, self.wrap_view('get_search'), name="api_get_search"),
            url(r"^(?P<resource_name>%s)\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('dispatch_list'), name="api_dispatch_list"),
            url(r"^(?P<resource_name>%s)/schema\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('get_schema'), name="api_get_schema"),
            url(r"^(?P<resource_name>%s)/datatables\.(?P<format>\w+)$" % self._meta.resource_name, self.wrap_view('get_datatables'), name="api_get_datatables"),
            url(r"^(?P<resource_name>%s)/set/(?P<%s_list>\w[\w/;-]*)\.(?P<format>\w+)$" % (self._meta.resource_name,  self._meta.detail_uri_name), self.wrap_view('get_multiple'), name="api_get_multiple"),
            url(r"^(?P<resource_name>%s)/(?P<%s>\w[\w/-]*)\.(?P<format>\w+)$" % (self._meta.resource_name, self._meta.detail_uri_name), self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

# ----------------------------------------------------------------------------------------------------------------------


class ActivitySuppResource(ChemblModelResource):
    class Meta(ChemblResourceMeta):
        queryset = ActivitySupp.objects.all()
        resource_name = 'activity_supplementary_data'
        collection_name = 'activity_supplementary_data'
        serializer = ChEMBLApiSerializer(resource_name, {collection_name: resource_name})
        fields = (
            'as_id',
            'rgid',
            'smid',
            'type',
            'relation',
            'value',
            'units',
            'text_value',
            'standard_type',
            'standard_relation',
            'standard_value',
            'standard_units',
            'standard_text_value',
            'comments',
        )


class ActivitySuppByActivityResource(ChemblModelResource):

    bao_format = fields.CharField('assay__bao_format_id', null=True, blank=True)
    bao_label = fields.CharField('assay__bao_format__label', null=True, blank=True)
    bao_endpoint = fields.CharField('bao_endpoint_id', null=True, blank=True)
    data_validity_description = fields.CharField('data_validity_comment__description', null=True, blank=True)
    data_validity_comment = fields.CharField('data_validity_comment__data_validity_comment', null=True, blank=True)
    document_chembl_id = fields.CharField('doc__chembl_id', null=True, blank=True)
    molecule_chembl_id = fields.CharField('molecule__chembl_id', null=True, blank=True)
    molecule_pref_name = fields.CharField('molecule__pref_name', null=True, blank=True)
    parent_molecule_chembl_id = fields.CharField('molecule__moleculehierarchy__parent_molecule__chembl_id', null=True, blank=True)
    target_chembl_id = fields.CharField('assay__target__chembl_id', null=True, blank=True)
    target_pref_name = fields.CharField('assay__target__pref_name', null=True, blank=True)
    target_organism = fields.CharField('assay__target__organism', null=True, blank=True)
    target_tax_id = fields.CharField('assay__target__tax_id', null=True, blank=True)
    assay_chembl_id = fields.CharField('assay__chembl_id', null=True, blank=True)
    assay_type = fields.CharField('assay__assay_type__assay_type', null=True, blank=True)
    src_id = fields.IntegerField('src_id', null=True, blank=True)
    assay_description = fields.CharField('assay__description', null=True, blank=True)
    document_year = fields.IntegerField('doc__year', null=True, blank=True)
    document_journal = fields.CharField('doc__journal', null=True, blank=True)
    record_id = fields.IntegerField('record_id', null=True, blank=True)
    canonical_smiles = fields.CharField('molecule__compoundstructures__canonical_smiles', null=True, blank=True)
    ligand_efficiency = fields.ForeignKey('chembl_webservices.resources.activities.LigandEfficiencyResource',
                                            'ligandeff', full=True, null=True, blank=True)
    activity_properties = fields.ToManyField('chembl_webservices.resources.activities.ActivityPropertiesResource', 'activityproperties_set', full=True, null=True, blank=True)

    supplementary_data = fields.ToManyField('chembl_webservices.resources.activities.ActivitySuppResource', 'activity_supps', full=True, null=True, blank=True)

    class Meta(ChemblResourceMeta):
        queryset = Activities.objects.filter(activitysuppmap__isnull=False).distinct()
        resource_name = 'activity_supplementary_data_by_activity'
        collection_name = 'activity_supplementary_data_by_activity'
        serializer = ChEMBLApiSerializer(resource_name, {collection_name: resource_name, 'activity_properties': 'activity_properties', 'supplementary_data': 'activity_smid'})
        prefetch_related = [
                            Prefetch(
                                'activity_supps'
                            ),
                            Prefetch('assay', queryset=Assays.objects.only('description', 'chembl', 'assay_id',
                                                                           'target', 'assay_type',
                                                                           'bao_format')),
                            Prefetch('assay__assay_type', queryset=AssayType.objects.only('assay_type', 'assay_desc')),
                            Prefetch('assay__bao_format', queryset=BioassayOntology.objects.only('bao_id', 'label')),
                            Prefetch('assay__target', queryset=TargetDictionary.objects.only('pref_name', 'chembl',
                                                                                             'organism', 'tid',
                                                                                             'tax_id')),
                            Prefetch('doc', queryset=Docs.objects.only('year', 'journal', 'chembl')),
                            Prefetch('ligandeff'),
                            Prefetch('molecule', queryset=MoleculeDictionary.objects.only('chembl')),
                            Prefetch('molecule__compoundstructures',
                                     queryset=CompoundStructures.objects.only('canonical_smiles')),
                            Prefetch('molecule__moleculehierarchy'),
                            Prefetch('molecule__moleculehierarchy__parent_molecule',
                                     queryset=MoleculeDictionary.objects.only('chembl')),
                            Prefetch('data_validity_comment',
                                     queryset=DataValidityLookup.objects.only('description', 'data_validity_comment')),
                            Prefetch('activityproperties_set'),
                            ]
        fields = (
            'supplementary_data',
            'activity_comment',
            'activity_id',
            'assay_chembl_id',
            'assay_description',
            'assay_type',
            'src_id',
            'bao_endpoint',
            'bao_format'
            'canonical_smiles',
            'data_validity_comment',
            'document_journal',
            'document_year',
            'document_chembl_id',
            'molecule_chembl_id',
            'molecule_pref_name',
            'parent_molecule_chembl_id',
            'pchembl_value',
            'potential_duplicate',
            'qudt_units',
            'record_id',
            'relation',
            'standard_flag',
            'standard_relation',
            'standard_text_value',
            'standard_type',
            'standard_units',
            'standard_upper_value',
            'standard_value',
            'target_pref_name',
            'target_organism',
            'text_value',
            'toid',
            'type',
            'units',
            'uo_units',
            'upper_value',
            'value',
        )
