import os
import os.path as op

from pyrevit import PyRevitException
from pyrevit.coreutils import get_all_subclasses
from pyrevit.coreutils.logger import get_logger


logger = get_logger(__name__)


def _get_discovered_comps(comp_path, component_types_list):
    discovered_cmps = []
    logger.debug('Testing _get_component(s) on: {} '.format(comp_path))
    # comp_path might be a file or a dir,
    # but its name should not start with . or _:
    for component_type in component_types_list:
        logger.debug('Testing sub_directory {} for {}'
                     .format(comp_path, component_type))
        try:
            # if cmp_class can be created for this sub-dir, the add to list
            # cmp_class will raise error if comp_path is not of cmp_class type.
            component = component_type()
            component.__init_from_dir__(comp_path)
            discovered_cmps.append(component)
            logger.debug('Successfuly created component: {} from: {}'
                         .format(component, comp_path))
            break
        except PyRevitException:
            logger.debug('Can not create component of type: {} from: {}'
                         .format(component_type, comp_path))

    return discovered_cmps


def _create_subcomponents(search_dir,
                          component_types_list,
                          create_from_search_dir=False):
    """
    Parses the provided directory and returns a list of objects of the
    types in component_types_list.

    Arguments:
        search_dir: directory to parse
        component_types_list: This methods checks the subfolders in search_dir
                              against the _get_component types provided
        in this list.

    Example:
        _create_subcomponents(search_dir,
                              [LinkButton, PushButton, or ToggleButton])
        this method creates LinkButton, PushButton, or ToggleButton for 
        the parsed sub-directories under search_dir with matching .type_id
        identifiers in their names. (e.g. "folder.LINK_BUTTON_POSTFIX")

    Returns:
        list of created classes of types provided in component_types_list
    """
    sub_cmp_list = []

    if not create_from_search_dir:
        logger.debug('Searching directory: {} for components of type: {}'
                     .format(search_dir, component_types_list))
        for file_or_dir in os.listdir(search_dir):
            full_path = op.join(search_dir, file_or_dir)
            if not file_or_dir.startswith(('.', '_')):
                sub_cmp_list.extend(_get_discovered_comps(full_path,
                                                          component_types_list))
            else:
                logger.debug('Skipping _get_component. '
                             'Name can not start with . or _: {}'
                             .format(full_path))
    else:
        sub_cmp_list.extend(_get_discovered_comps(search_dir,
                                                  component_types_list))

    return sub_cmp_list


def _parse_for_components(component):
    """Recursively parses _get_component.directory for components of type
    _get_component.allowed_sub_cmps. This method uses get_all_subclasses() to
    get a list of all subclasses of _get_component.allowed_sub_cmps type.
    This ensures that if any new type of component_class is added later,
    this method does not need to be updated as the new sub-class will be
    listed by .__subclasses__() method of the parent class and this method
    will check the directory for its .type_id
    """
    for new_cmp in _create_subcomponents(
            component.directory,
            get_all_subclasses(component.allowed_sub_cmps)):
        # add the successfulyl created _get_component to the
        # parent _get_component
        component.add_component(new_cmp)
        if new_cmp.is_container:
            # Recursive part: parse each sub-_get_component
            # for its allowed sub-sub-components.
            _parse_for_components(new_cmp)


def parse_comp_dir(comp_path, comp_class):
    return _create_subcomponents(comp_path, get_all_subclasses([comp_class]),
                                 create_from_search_dir=True)


def get_parsed_extension(extension):
    """
    Parses package directory and creates and adds components to the package
    object. Each package object is the root to a tree of components that exists
    under that package. (e.g. tabs, buttons, ...) sub components of package
    can be accessed by iterating the _get_component.
    See _basecomponents for types.
    """
    _parse_for_components(extension)
    return extension


def parse_dir_for_ext_type(root_dir, parent_cmp_type):
    """
    Parses root_dir and return a list of objects of type parent_cmp_type
    for installed extensions. The package objects won't be parsed at this level.
    This is useful for collecting basic info on an extension type
    for cache cheching or updating extensions using their directory paths.
    """
    # making sure the provided directory exists.
    # This is mainly for the user defined package directories
    if not op.exists(root_dir):
        logger.debug('Extension search directory does not exist: {}'
                     .format(root_dir))
        return []

    # try creating extensions in given directory
    ext_data_list = []

    logger.debug('Parsing directory for extensions of type: {}'
                 .format(parent_cmp_type))
    for ext_data in _create_subcomponents(root_dir, [parent_cmp_type]):
        logger.debug('Extension directory found: {}'.format(ext_data))
        ext_data_list.append(ext_data)

    return ext_data_list
