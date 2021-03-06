# -*- coding: utf-8 -*-
"""
/***************************************************************************
 QRVT
                                 A QGIS plugin
 Wrapper for the RVT
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2018-11-30
        copyright            : (C) 2018 by covigeos e.U.
        email                : s.floery@covigeos.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load QRVT class from file QRVT.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .q_rvt import QRVT
    return QRVT(iface)
