# -*- coding: utf-8 -*-
"""
/***************************************************************************
 StormHelpClassDockWidget
                                 A QGIS plugin
 The Storm Help plugin provides help in case of a storm
                             -------------------
        begin                : 2017-01-07
        git sha              : $Format:%H$
        copyright            : (C) 2017 by Raphael Sulzer
        email                : raphaelsulzer@gmx.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

import os

from PyQt4 import QtGui, QtCore, uic
from qgis.core import *
from qgis.core import QgsGeometry, QgsMapLayerRegistry
# from PyQt4 import QtCore
# from PyQt4 import QtGui

from qgis.gui import *
from qgis.gui import QgsMapTool
from qgis.networkanalysis import *

from PyQt4.QtGui import QCursor, QPixmap
from PyQt4.QtCore import Qt
from PyQt4.QtCore import pyqtSignal
from . import utility_functions as uf

import processing
import random

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'storm_help_dockwidget_base.ui'))



class MapToolEmitPoint(QgsMapToolEmitPoint):
    canvasDoubleClicked = QtCore.pyqtSignal(object, object)

    def canvasDoubleClickEvent(self, event):
        point = self.toMapCoordinates(event.pos())
        self.canvasDoubleClicked.emit(point, event.button())
        super(MapToolEmitPoint, self).canvasDoubleClickEvent(event)





class StormHelpClassDockWidget(QtGui.QDockWidget, FORM_CLASS, QgsMapTool, QgsMapLayerRegistry):

    closingPlugin = pyqtSignal()

    def __init__(self, iface, parent=None):
        """Constructor."""
        super(StormHelpClassDockWidget, self).__init__(parent)
        #super(QgsMapTool, self).__init__(canvas)

        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        # define globals
        self.iface = iface
        self.canvas = self.iface.mapCanvas()


        layer = uf.getLegendLayerByName(self.iface, "Emergencies")

        self.canvas.setLayerSet([QgsMapCanvasLayer(layer)])


        #GUI
        self.Pages.setCurrentIndex(0)
        uf.showMessage(self.iface, 'Strong winds! Keep out of red marked areas!', type='Info', lev=1, dur=10)

        # change pages
        self.button_startNew.clicked.connect(self.startNew)
        self.button_startNew2.clicked.connect(self.startNew)
        self.button_startNew3.clicked.connect(self.startNew)
        self.button_startNew4.clicked.connect(self.startNew)
        self.button_startNew5.clicked.connect(self.startNew)
        self.button_startNew5.clicked.connect(self.startNew)
        self.button_startNew6.clicked.connect(self.startNew)
        self.button_startNew7.clicked.connect(self.startNew)
        self.button_startNew8.clicked.connect(self.startNew)
        self.button_startNew9.clicked.connect(self.startNew)
        self.button_startNew10.clicked.connect(self.startNew)
        self.button_startNew11.clicked.connect(self.startNew)
        self.button_startNew12.clicked.connect(self.startNew)
        self.button_startNew13.clicked.connect(self.startNew)
        self.button_startNew14.clicked.connect(self.startNew)
        self.button_startNew15.clicked.connect(self.startNew)




        self.button_provideInformation.clicked.connect(self.provideInformation)

        self.button_helpAtEmergency.clicked.connect(self.randLocation2)




        # actions
        self.toolPan = QgsMapToolPan(self.canvas)
        self.toolZoom = QgsMapToolZoom(self.canvas, 0)
        self.canvas.setMapTool(self.toolZoom)

        self.emitPoint = QgsMapToolEmitPoint(self.canvas)
        self.emitPoint.canvasClicked.connect(self.getPoint)

        maptool = MapToolEmitPoint(self.canvas)
        self.canvas.setMapTool(maptool)
        maptool.canvasDoubleClicked.connect(self.handleDoubleClick)


        # page 0 - choose to give or take help
        self.button_needHelp.clicked.connect(self.needHelp)
        self.button_needHelp.setStyleSheet("font: bold 14px;")

        self.button_wantToHelp.clicked.connect(self.wantToHelp)
        self.button_wantToHelp.setStyleSheet("font: bold 14px;")

        self.button_showWeather.setIcon(QtGui.QIcon(':/plugins/StormHelpClass/icons/weather3.PNG'))


        # page 1 - leave or stay
        self.button_leave.clicked.connect(self.leaveLocation)
        self.button_stay.clicked.connect(self.stayLocation)
        self.button_showWeather2.setIcon(QtGui.QIcon(':/plugins/StormHelpClass/icons/weather3.PNG'))


        # page 2
        self.button_correctLocation.clicked.connect(self.determineAction)
        self.button_wrongLocation.clicked.connect(self.activateLocalization)
        #self.button_wrongLocation.setStyleSheet("background-color: blue; color: white")

        self.smallCanvas = self.QgsMapCanvas
        self.smallMap()


        # page 3 - choose destination of route
        self.button_searchStreet.clicked.connect(self.searchStreet)
        self.inputStreet.setText('Streetname')

        self.button_chooseEnd.clicked.connect(self.chooseEnd)

        self.button_endChosen.clicked.connect(self.buildNetwork)
        self.button_endChosen.clicked.connect(self.calculateRoute)

        # page 4 - choose to report blocking or help out at an emergency
        self.button_reportBlocking.clicked.connect(self.reportBlocking)
        self.button_showWeather3.setIcon(QtGui.QIcon(':/plugins/StormHelpClass/icons/weather3.PNG'))


        # page 5 - choose and save blocking
        self.button_chooseRoad.clicked.connect(self.activateLocalization)
        self.button_saveBlocking.clicked.connect(self.saveBlocking)


        # page 6 - where are you (to report your emergency)
        self.button_correctLocation2.clicked.connect(self.determineAction)
        self.button_wrongLocation2.clicked.connect(self.activateLocalization)

        # page 7 - call 112
        self.button_call112.clicked.connect(self.call112)

        # page 8 - calling 112
        self.policeLabel.setPixmap(QtGui.QPixmap(':/plugins/StormHelpClass/icons/112.PNG'))


        # page 9 - provide additional information
        self.button_saveInformation.clicked.connect(self.saveInformation)

        # page 10 - where are you (to start helping out)
        self.button_correctLocation10.clicked.connect(self.showEmergency)
        self.button_wrongLocation10.clicked.connect(self.activateLocalization)
        self.smallCanvas = self.QgsMapCanvas4
        self.smallMap()

        # page 11 - choose emergency and calculate route
        self.table_emergencies.cellClicked.connect(self.selectSelectedItem)
        self.button_calculateRoute2.clicked.connect(self.buildNetwork)
        self.button_calculateRoute2.clicked.connect(self.calculateRoute)
        self.button_deleteEmergencyCheck.clicked.connect(self.deleteEmergencyCheck)


        # page 12 - choose safehouse, hospital or other destination
        self.button_showOther.clicked.connect(self.showOther)
        self.button_showShelter.clicked.connect(self.showShelter)
        self.button_showHospital.clicked.connect(self.showHospital)

        self.button_showShelter.setIcon(QtGui.QIcon(':/plugins/StormHelpClass/icons/house.png'))
        self.button_showHospital.setIcon(QtGui.QIcon(':/plugins/StormHelpClass/icons/cross.png'))


        # page 13 - shelters
        self.table_shelter.cellClicked.connect(self.selectSelectedItem)
        self.button_calculateRoute13.clicked.connect(self.buildNetwork)
        self.button_calculateRoute13.clicked.connect(self.calculateRoute)


        # page 14 - hospitals
        self.table_hospital.cellClicked.connect(self.selectSelectedItem)
        self.button_calculateRoute14.clicked.connect(self.buildNetwork)
        self.button_calculateRoute14.clicked.connect(self.calculateRoute)


        # page 15 - delete emergency
        self.button_deleteEmergency.clicked.connect(self.deleteEmergency)
        self.button_notDeleteEmergency.clicked.connect(self.notDeleteEmergency)



    def handleDoubleClick(self, point, buttons):
        print('doubleclick')

    def showEvent(self, event):

        self.Pages.setCurrentIndex(0)

        scenario_open = False
        scenario_file = os.path.join(os.path.dirname(__file__),'sample_data','project_file2.qgs')
        # check if file exists
        if os.path.isfile(scenario_file):
            self.iface.addProject(scenario_file)
            scenario_open = True
        else:
            last_dir = uf.getLastDir("StormHelpClass")
            new_file = QtGui.QFileDialog.getOpenFileName(self, "", last_dir, "(*.qgs)")
            if new_file:
                self.iface.addProject(unicode(new_file))
                scenario_open = True


    def closeEvent(self, event):
        self.closingPlugin.emit()
        event.accept()



    # visualization

    def zoomToSelectedFeature(self, scale, layer):


        box = layer.boundingBoxOfSelected()

        box.scale(scale)

        self.canvas.setExtent(box)
        self.canvas.refresh()




    # user interaction (clicking buttons)

    # all pages

    def startNew(self):

        self.Pages.setCurrentIndex(0)

        self.canvas.setMapTool(self.toolZoom)


        # list of layers that should be removed
        remove_layer = ["Routes", "Buffer", "emergency_temp", "location", "destination", "obstacle_temp", "Temp_Network"]

        #remove_selection_layers = []

        # remove selection on all layers
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        for layer in layers:

            try:
                layer.removeSelection()

            except:
                pass

            if layer.name() in remove_layer:

                QgsMapLayerRegistry.instance().removeMapLayers([layer])

        roads_layer = uf.getLegendLayerByName(self.iface, "Roads")

        self.canvas.setExtent(roads_layer.extent())

        self.canvas.zoomByFactor(0.98)

        self.inputStreet.setText('Streetname')

        #self.buff()


    def determineAction(self):

        # this function determines further action after location selection, based on the current index of the QStackedWidget (so based on the current page)

        if self.Pages.currentIndex() == 2:

            # select second point for routing/ end street for routing

            roads_layer = uf.getLegendLayerByName(self.iface, "Roads")

            self.iface.setActiveLayer(roads_layer)

            self.canvas.setMapTool(self.toolPan)

            #self.Pages.setCurrentIndex(3)
            self.Pages.setCurrentIndex(12)

        elif self.Pages.currentIndex() == 4:

            pass

            self.reportBlockade()


            #print('current index is 2')

        elif self.Pages.currentIndex() == 6:

            self.saveEmergency()


    # page 0
    def needHelp(self):

        self.Pages.setCurrentIndex(1)
    def wantToHelp(self):

        self.Pages.setCurrentIndex(4)


    # page 1
    def leaveLocation(self):

        self.randLocation2()
        self.canvas.setMapTool(self.toolPan)
        self.Pages.setCurrentIndex(2)

    def stayLocation(self):

        self.randLocation2()
        self.canvas.setMapTool(self.toolPan)
        self.Pages.setCurrentIndex(6)


    # page 2

    def smallMap(self):
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        canvas_layers = []
        for layer in layers:
            canvas_layers.append(QgsMapCanvasLayer(layer))


        self.smallCanvas.setLayerSet(canvas_layers)
        location_layer = uf.getLegendLayerByName(self.iface, "location")
        self.iface.setActiveLayer(location_layer)
        self.smallCanvas.zoomToSelected()
        self.smallCanvas.zoomByFactor(0.1)


    # page 7
    def call112(self):

        self.Pages.setCurrentIndex(8)


    # page 10
    # populate table
    def showEmergency(self):

        self.Pages.setCurrentIndex(11)

        emergency_layer = uf.getLegendLayerByName(self.iface, "Emergencies")

        # get start point from location layer
        location_layer = uf.getLegendLayerByName(self.iface, "location")
        startFeat = uf.getLastFeature(location_layer)
        startPoint = startFeat.geometry().centroid().asPoint()

        # populate table
        values = []
        # only use the first attribute in the list
        for feature in emergency_layer.getFeatures():

            dist = feature.geometry().distance(QgsGeometry.fromPoint(startPoint))
            dist = dist/1000
            name = str(feature.attributes()[1])
            type = str(feature.attributes()[0])
            nOfPeople = str(feature.attributes()[2])
            address = str(feature.attributes()[3])
            phone = str(feature.attributes()[4])



            values.append((name, type, nOfPeople, address, phone, dist, feature.id()))

        values.sort(key=lambda element: element[5], reverse=False)



        self.table_emergencies.clear()
        self.table_emergencies.setColumnCount(7)
        self.table_emergencies.setHorizontalHeaderLabels(["Name","Type", "No of People", "Address", "Phone", "Distance [km]", "ID"])
        self.table_emergencies.setRowCount(len(values))
        for i, item in enumerate(values):
            # i is the table row, items mus tbe added as QTableWidgetItems
            self.table_emergencies.setItem(i,0,QtGui.QTableWidgetItem(str(item[1])))
            self.table_emergencies.setItem(i, 1, QtGui.QTableWidgetItem("{:.1f}".format(item[5])))
            self.table_emergencies.setItem(i, 2, QtGui.QTableWidgetItem(str(item[3])))
            self.table_emergencies.setItem(i,3,QtGui.QTableWidgetItem(item[0]))
            self.table_emergencies.setItem(i, 4, QtGui.QTableWidgetItem(str(item[4])))
            self.table_emergencies.setItem(i, 5, QtGui.QTableWidgetItem(str(item[2])))
            self.table_emergencies.setItem(i, 6, QtGui.QTableWidgetItem(str(item[6])))
        self.table_emergencies.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        self.table_emergencies.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.ResizeToContents)
        self.table_emergencies.horizontalHeader().setResizeMode(2, QtGui.QHeaderView.ResizeToContents)
        self.table_emergencies.horizontalHeader().setResizeMode(3, QtGui.QHeaderView.ResizeToContents)
        self.table_emergencies.horizontalHeader().setResizeMode(4, QtGui.QHeaderView.ResizeToContents)
        self.table_emergencies.horizontalHeader().setResizeMode(5, QtGui.QHeaderView.ResizeToContents)
        self.table_emergencies.horizontalHeader().setResizeMode(6, QtGui.QHeaderView.ResizeToContents)
        #self.table_hospital.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
        self.table_emergencies.resizeRowsToContents()
        self.table_emergencies.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        # select first/closest item

        cols = self.table_emergencies.columnCount()
        for i in range(cols):

            item1 = self.table_emergencies.item(0, i)
            item1.setSelected(True)

        self.selectSelectedItem()

    # page 11 - emergencies
    def deleteEmergencyCheck(self):
        self.Pages.setCurrentIndex(15)


    # page 12
    def showOther(self):

        roads_layer = uf.getLegendLayerByName(self.iface, "Roads")

        self.iface.setActiveLayer(roads_layer)

        self.canvas.setMapTool(self.toolPan)

        self.Pages.setCurrentIndex(3)

    # populate table
    def showShelter(self):

        self.Pages.setCurrentIndex(13)

        shelter_layer = uf.getLegendLayerByName(self.iface, "Shelters")

        # get start point from location layer
        location_layer = uf.getLegendLayerByName(self.iface, "location")
        startFeat = uf.getLastFeature(location_layer)
        startPoint = startFeat.geometry().centroid().asPoint()

        # populate table
        values = []
        # only use the first attribute in the list
        for feature in shelter_layer.getFeatures():

            dist = feature.geometry().distance(QgsGeometry.fromPoint(startPoint))
            dist = dist/1000

            type = str(feature.attributes()[2])
            name = str(feature.attributes()[3])

            if str(name) == 'NULL':
                name = type
            namename = name + '\n' + '(' + type + ')'
            values.append((feature.id(), namename, dist))

        values.sort(key=lambda element: element[2], reverse=False)

        self.table_shelter.clear()
        self.table_shelter.setColumnCount(3)
        self.table_shelter.setHorizontalHeaderLabels(["Name","Distance [km]", "ID"])
        self.table_shelter.setRowCount(len(values))
        for i, item in enumerate(values):
            # i is the table row, items mus tbe added as QTableWidgetItems
            self.table_shelter.setItem(i,0,QtGui.QTableWidgetItem(item[1]))
            self.table_shelter.setItem(i,1,QtGui.QTableWidgetItem("{:.1f}".format(item[2])))
            self.table_shelter.setItem(i, 2, QtGui.QTableWidgetItem(str(item[0])))
        self.table_shelter.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        #self.table_shelter.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
        self.table_shelter.resizeRowsToContents()
        self.table_shelter.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)


        # select first/closest item, or better whole row
        cols = self.table_shelter.columnCount()
        for i in range(cols):

            item1 = self.table_shelter.item(0, i)
            item1.setSelected(True)

        self.selectSelectedItem()

    # populate table
    def showHospital(self):

        self.Pages.setCurrentIndex(14)

        hospital_layer = uf.getLegendLayerByName(self.iface, "Hospitals")

        # get start point from location layer
        location_layer = uf.getLegendLayerByName(self.iface, "location")
        startFeat = uf.getLastFeature(location_layer)
        startPoint = startFeat.geometry().centroid().asPoint()

        # populate table
        values = []
        # only use the first attribute in the list
        for feature in hospital_layer.getFeatures():

            dist = feature.geometry().distance(QgsGeometry.fromPoint(startPoint))
            dist = dist/1000

            name = str(feature.attributes()[3])

            values.append((feature.id(), name, dist))

        values.sort(key=lambda element: element[2], reverse=False)

        self.table_hospital.clear()
        self.table_hospital.setColumnCount(3)
        self.table_hospital.setHorizontalHeaderLabels(["Name","Distance [km]", "ID"])
        self.table_hospital.setRowCount(len(values))
        for i, item in enumerate(values):
            # i is the table row, items mus tbe added as QTableWidgetItems
            self.table_hospital.setItem(i,0,QtGui.QTableWidgetItem(item[1]))
            self.table_hospital.setItem(i,1,QtGui.QTableWidgetItem("{:.1f}".format(item[2])))
            self.table_hospital.setItem(i, 2, QtGui.QTableWidgetItem(str(item[0])))
        self.table_hospital.horizontalHeader().setResizeMode(0, QtGui.QHeaderView.ResizeToContents)
        #self.table_hospital.horizontalHeader().setResizeMode(1, QtGui.QHeaderView.Stretch)
        self.table_hospital.resizeRowsToContents()
        self.table_hospital.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)

        # select first/closest item, or better whole row
        cols = self.table_hospital.columnCount()
        for i in range(cols):

            item1 = self.table_hospital.item(0, i)
            item1.setSelected(True)

        self.selectSelectedItem()



    # page 15 - delete emergency
    def deleteEmergency(self):

        emergency_layer = uf.getLegendLayerByName(self.iface, "Emergencies")

        emergency_layer.startEditing()

        emergency_layer.deleteSelectedFeatures()

        emergency_layer.commitChanges()

        self.canvas.refresh()

        self.showEmergency()

        self.Pages.setCurrentIndex(11)

        uf.showMessage(self.iface, 'The emergency has been removed from the list!', type='Info', lev=3, dur=4)






    def notDeleteEmergency(self):

        self.Pages.setCurrentIndex(11)





    # localization
    def randLocation2(self):

        emergency_layer = uf.getLegendLayerByName(self.iface, "Emergencies")

        rand_location = uf.createTempLayer('location', 'POINT', emergency_layer.crs().postgisSrid(), [], [])


        feat = QgsFeature(rand_location.pendingFields())

        rand_x = random.randrange(84500, 100700, 1)
        rand_y = random.randrange(428500, 443900, 1)

        #rand_x = 99918
        #rand_y = 430193

        rand_point = QgsPoint(rand_x, rand_y)

        feat.setGeometry(QgsGeometry.fromPoint(rand_point))

        rand_location.dataProvider().addFeatures([feat])

        uf.loadTempLayer(rand_location)

        feat = uf.getLastFeature(rand_location)

        rand_location.removeSelection()
        rand_location.select(feat.id())

        self.canvas.zoomToSelected()
        self.canvas.zoomByFactor(0.1)

        symbol = QgsMarkerSymbolV2.createSimple({'name': 'circle', 'color': 'yellow'})
        symbol.setSize(3)
        rand_location.rendererV2().setSymbol(symbol)

        self.canvas.refresh()

        if self.Pages.currentIndex() == 4:

            self.Pages.setCurrentIndex(10)



    # get the point when the user clicks on the canvas
    def activateLocalization(self):
        # remember currently selected tool
        self.userTool = self.canvas.mapTool()
        # activate coordinate capture tool
        self.canvas.setMapTool(self.emitPoint)


    def getPoint(self, mapPoint, mouseButton):
        # change tool so you don't get more than one POI
        #self.canvas.unsetMapTool(self.emitPoint)
        #self.canvas.setMapTool(self.userTool)

        # Get the click
        if mapPoint:

            # choose first location                # choose location to help out
            if self.Pages.currentIndex() == 2 or self.Pages.currentIndex() == 10:

                randloc_layer = uf.getLegendLayerByName(self.iface, "location")

                self.chooseLocation(randloc_layer, mapPoint)


            # choose destination
            elif self.Pages.currentIndex() == 3 or self.Pages.currentIndex() == 11:

                roads_layer = uf.getLegendLayerByName(self.iface, "Roads")
                roads_layer.removeSelection()
                destination_layer = uf.getLegendLayerByName(self.iface, "destination")

                if destination_layer:

                    self.chooseLocation(destination_layer, mapPoint)

                else:

                    emergency_layer = uf.getLegendLayerByName(self.iface, "Emergencies")

                    destination_layer = uf.createTempLayer('destination', 'POINT', emergency_layer.crs().postgisSrid(), [], [])

                    symbol = QgsMarkerSymbolV2.createSimple({'name': 'circle', 'color': 'red'})
                    symbol.setSize(3)
                    destination_layer.rendererV2().setSymbol(symbol)

                    self.chooseLocation(destination_layer, mapPoint)


            # choose emergency location
            elif self.Pages.currentIndex() == 6:


                self.dispEmergency(mapPoint)


            # choose blocking location
            elif self.Pages.currentIndex() == 5:

                obstacle_temp = uf.getLegendLayerByName(self.iface, "obstacle_temp")
                roads_layer = uf.getLegendLayerByName(self.iface, "Roads")

                if not obstacle_temp:

                    obstacle_layer = uf.getLegendLayerByName(self.iface, "Obstacles")

                    obstacle_temp = uf.createTempLayer('obstacle_temp', 'POINT', obstacle_layer.crs().postgisSrid(), [], [])
                    symbol = QgsMarkerSymbolV2.createSimple({'name': 'circle', 'color': 'yellow'})
                    symbol.setSize(3)
                    obstacle_temp.rendererV2().setSymbol(symbol)

                # get featID of closest road
                featID = self.nearestFeature(mapPoint)

                feat = uf.getFeatureById(roads_layer, featID)

                blockedPoint = feat.geometry().centroid().asPoint()

                self.chooseLocation(obstacle_temp, blockedPoint)




    def chooseLocation(self, layer, mapPoint):


        layer.startEditing()

        if layer.featureCount() > 0 and layer.name() != "obstacle_temp":
            feat_old = uf.getLastFeature(layer)
            layer.deleteFeature(feat_old.id())

        feat_new = QgsFeature(layer.pendingFields())
        feat_new.setGeometry(QgsGeometry.fromPoint(mapPoint))
        layer.dataProvider().addFeatures([feat_new])
        uf.loadTempLayer(layer)
        layer.commitChanges()

        self.canvas.refresh()



    def chooseEnd(self):

        self.activateLocalization()


    def searchStreet(self):

        roads_layer = uf.getLegendLayerByName(self.iface, "Roads")
        roads_layer.removeSelection()

        street = self.inputStreet.text()

        print(street)

        roads_layer = uf.getLegendLayerByName(self.iface, "Roads")

        roads_layer.removeSelection()

        feat = uf.getFeaturesByListValues(roads_layer, 'stt_naam', [street])

        if not feat:

            uf.showMessage(self.iface, 'Street not found. Try again!', type='Info', lev=2, dur=4)

            return

        else:

            sfeat = feat.iterkeys().next()

        print(sfeat)

        roads_layer.select(sfeat)

        #mapPoint = sfeat.geometry().centroid().asPoint()



        self.canvas.zoomToSelected()
        self.canvas.zoomByFactor(4)


    def nearestFeature(self, mapPoint):

        layerData = []

        layer = uf.getLegendLayerByName(self.iface, "Roads")

        if self.Pages.currentIndex() == 2 or self.Pages.currentIndex() == 6:

            layer.removeSelection()

        shortestDistance = float("inf")
        closestFeatureId = -1

        # Loop through all features in the layer
        for f in layer.getFeatures():
            dist = f.geometry().distance(QgsGeometry.fromPoint(mapPoint))
            #print(f.id())
            #print(dist)

            if dist < shortestDistance:
                shortestDistance = dist
                closestFeatureId = f.id()

        info = (layer, closestFeatureId, shortestDistance)
        layerData.append(info)



        if not len(layerData) > 0:
            # Looks like no vector layers were found - do nothing
            return

        # Sort the layer information by shortest distance
        layerData.sort(key=lambda element: element[2], reverse=False)

        # Select the closest feature
        layerWithClosestFeature, closestFeatureId, shortestDistance = layerData[0]
        #print(closestFeatureId)

        if self.Pages.currentIndex() == 5 or self.Pages.currentIndex() == 13 or self.Pages.currentIndex() == 14 or self.Pages.currentIndex() == 11:
            layerWithClosestFeature.select(closestFeatureId)

        return closestFeatureId



    # analysis

    def getNetwork(self):
        roads_layer = uf.getLegendLayerByName(self.iface, "Roads")
        if roads_layer:
            # see if there is an obstacles layer to subtract roads from the network
            obstacles_layer = uf.getLegendLayerByName(self.iface, "Obstacles")
            if obstacles_layer:
                print('yes there is an obstacle')

                # remove features by id here, from obstacle layer, where I give the obstacle features the same id that the corresponding road has


                # first dublicate the roads_layer
                feats = [feat for feat in roads_layer.getFeatures()]

                road_network = uf.createTempLayer('Temp_Network','LINESTRING',roads_layer.crs().postgisSrid(),[],[])

                mem_layer_data = road_network.dataProvider()
                attr = roads_layer.dataProvider().fields().toList()
                mem_layer_data.addAttributes(attr)
                road_network.updateFields()
                mem_layer_data.addFeatures(feats)
                #QgsMapLayerRegistry.instance().addMapLayer(road_network)

                road_network.startEditing()

                for obstacles in obstacles_layer.getFeatures():

                    feat = uf.getFeatureById(road_network, obstacles['streetID']+1)

                    road_network.select(feat.id())

                a=road_network.deleteSelectedFeatures()
                print(a)

                road_network.commitChanges()

            else:
                road_network = roads_layer
            return road_network
        else:
            return


    def buildNetwork(self):
        self.network_layer = self.getNetwork()

        road_layer = uf.getLegendLayerByName(self.iface, "Roads")


        location_layer = uf.getLegendLayerByName(self.iface, "location")
        startFeat = uf.getLastFeature(location_layer)
        startPoint = startFeat.geometry().centroid().asPoint()
        startID = self.nearestFeature(startPoint)

        destination_layer = uf.getLegendLayerByName(self.iface, "destination")
        if destination_layer:
            endFeat = uf.getLastFeature(destination_layer)
            endPoint = endFeat.geometry().centroid().asPoint()
            endID = self.nearestFeature(endPoint)
            print('yes dest')

            road_layer.select([startID, endID])

        else:
            # end is already selected by search street function
            road_layer.select([startID])

            print('attention: no destination!! if not selected by street search!!')


        if self.network_layer:
            # get the points to be used as origin and destination
            # in this case gets the centroid of the selected features
            selected_sources = road_layer.selectedFeatures()
            source_points = [feature.geometry().centroid().asPoint() for feature in selected_sources]
            # build the graph including these points
            if len(source_points) > 1:
                self.graph, self.tied_points = uf.makeUndirectedGraph(self.network_layer, source_points)
                # the tied points are the new source_points on the graph
                if self.graph and self.tied_points:
                    text = "network is built for %s points" % len(self.tied_points)
                    print(text)
        return


    def calculateRoute(self):
        self.canvas.setMapTool(self.toolPan)
        # origin and destination must be in the set of tied_points
        options = len(self.tied_points)
        if options > 1:
            # origin and destination are given as an index in the tied_points list
            origin = 0
            destination = random.randint(1,options-1)
            # calculate the shortest path for the given origin and destination
            path = uf.calculateRouteDijkstra(self.graph, self.tied_points, origin, destination)
            # store the route results in temporary layer called "Routes"
            routes_layer = uf.getLegendLayerByName(self.iface, "Routes")
            # create one if it doesn't exist
            if not routes_layer:
                attribs = ['id']
                types = [QtCore.QVariant.String]
                routes_layer = uf.createTempLayer('Routes','LINESTRING',self.network_layer.crs().postgisSrid(), attribs, types)
                uf.loadTempLayer(routes_layer)
            # insert route line
            for route in routes_layer.getFeatures():
                print route.id()
            uf.insertTempFeatures(routes_layer, [path], [['testing',100.00]])
            buffer = processing.runandload('qgis:fixeddistancebuffer',routes_layer,10.0,5,False,None)
            buffer_layer = uf.getLegendLayerByName(self.iface, "Buffer")

            symbols = buffer_layer.rendererV2().symbols()
            symbol = symbols[0]
            symbol.setColor(QtGui.QColor.fromRgb(50, 50, 250))
            self.canvas.refresh()
            #self.legendInterface().refreshLayerSymbology(self.vlayer)


        # zoom on route
        layer = uf.getLegendLayerByName(self.iface, "Roads")
        self.zoomToSelectedFeature(1.3, layer)

        layer.removeSelection()

    def reportBlocking(self):

        self.Pages.setCurrentIndex(5)


    def saveBlocking(self):


        roads_layer = uf.getLegendLayerByName(self.iface, "Roads")
        obstacles_layer = uf.getLegendLayerByName(self.iface, "Obstacles")
        obstacles_temp = uf.getLegendLayerByName(self.iface, "obstacle_temp")
        if obstacles_temp:
            QgsMapLayerRegistry.instance().removeMapLayers([obstacles_temp])

        selected_sources = roads_layer.selectedFeatures()

        print(selected_sources)

        source_points = [feature.geometry().centroid().asPoint() for feature in selected_sources]

        feat = []

        for i, road in enumerate(selected_sources):

            feat.append(QgsFeature(obstacles_layer.pendingFields()))

            feat[i].setAttribute('streetID', road.id())

            feat[i].setGeometry(QgsGeometry.fromPoint(source_points[i]))


        obstacles_layer.dataProvider().addFeatures(feat)

        roads_layer.removeSelection()


        self.canvas.refresh()

        uf.showMessage(self.iface, 'The blocking has been saved succesfully!', type='Info', lev=3, dur=4)

        self.startNew()



    def dispEmergency(self, mapPoint):

        # create temp layer with point

        location_layer = uf.getLegendLayerByName(self.iface, "location")
        QgsMapLayerRegistry.instance().removeMapLayers([location_layer])



        emergency_layer = uf.getLegendLayerByName(self.iface, "Emergencies")
        emergency_temp = uf.getLegendLayerByName(self.iface, "emergency_temp")


        if emergency_temp:

            QgsMapLayerRegistry.instance().removeMapLayers([emergency_temp])


        emergency_temp = uf.createTempLayer('emergency_temp', 'POINT', emergency_layer.crs().postgisSrid(), [], [])

        symbol = QgsMarkerSymbolV2.createSimple({'name': 'circle', 'color': 'yellow'})
        symbol.setSize(3)
        emergency_temp.rendererV2().setSymbol(symbol)


        #use this in the future:
        #insertTempFeatures(layer, coordinates, attributes)

        feat = QgsFeature(emergency_temp.pendingFields())

        feat.setGeometry(QgsGeometry.fromPoint(mapPoint))

        emergency_temp.dataProvider().addFeatures([feat])

        uf.loadTempLayer(emergency_temp)




    def saveEmergency(self):


        # first get the point, either from location or emergency_temp layer
        emergency_temp = uf.getLegendLayerByName(self.iface, "emergency_temp")
        location_layer = uf.getLegendLayerByName(self.iface, "location")

        if location_layer:
            point = location_layer.getFeatures().next()
            QgsMapLayerRegistry.instance().removeMapLayers([location_layer])
        else:
            point = emergency_temp.getFeatures().next()
            QgsMapLayerRegistry.instance().removeMapLayers([emergency_temp])


        # now safe in (permanent) emergency layer
        emergency_layer = uf.getLegendLayerByName(self.iface, "Emergencies")
        emergency_layer.dataProvider().addFeatures([point])
        emergency_layer.dataProvider().updateExtents()
        self.iface.setActiveLayer(emergency_layer)
        self.canvas.refresh()
        uf.showMessage(self.iface, 'Your emergency has been added to the list!', type='Info', lev=3, dur=4)

        self.Pages.setCurrentIndex(7)


    def provideInformation(self):

        self.Pages.setCurrentIndex(9)
        print('provide further information')


    def saveInformation(self):

        emergency_layer = uf.getLegendLayerByName(self.iface, "Emergencies")

        # req = QgsFeatureRequest()
        #
        # req.setFilterFid(emergency_layer.allFeatureIds()[-1])
        #
        # feat = emergency_layer.getFeatures(req).next()

        feat = uf.getLastFeature(emergency_layer)

        emergency_layer.startEditing()


        emergency_layer.changeAttributeValue(feat.id(), 0, self.input_description.document().toPlainText())
        emergency_layer.changeAttributeValue(feat.id(), 1, self.input_name.text())
        emergency_layer.changeAttributeValue(feat.id(), 2, self.input_nOfPeople.value())
        emergency_layer.changeAttributeValue(feat.id(), 3, self.input_address.text())
        emergency_layer.changeAttributeValue(feat.id(), 4, self.input_phone.text())

        emergency_layer.commitChanges()

        self.canvas.refresh()

        uf.showMessage(self.iface, 'Your information has been saved succesfully!', type='Info', lev=3, dur=4)
        #self.startNew()



    # def chooseEmergency(self):
    #
    #     emergency_layer = uf.getLegendLayerByName(self.iface, "Emergencies")
    #
    #
    #     emergency_layer.selectAll()
    #
    #     box = emergency_layer.boundingBoxOfSelected()
    #
    #     self.canvas.setExtent(box)
    #
    #     emergency_layer.removeSelection()
    #
    #     self.activateLocalization()



    def buff(self):


        road_layer = uf.getLegendLayerByName(self.iface, "Roads")

        self.iface.setActiveLayer(road_layer)

        for feat in road_layer.getFeatures():

        # road_layer.select(22667)
        #
        # origins = road_layer.selectedFeatures()


            uf.calculateBuffer(self.iface, road_layer, [feat], 10)

        buffer_layer = uf.getLegendLayerByName(self.iface, "Buffer")

        tree_layer = uf.getLegendLayerByName(self.iface, "2016_Rotterdam_trees")

        uf.selectFeaturesByIntersection(tree_layer, buffer_layer, True)

        nOfTrees = tree_layer.selectedFeatureCount()

        print(nOfTrees)

        road_layer.startEditing()


        road_layer.changeAttributeValue(22667, 45, nOfTrees)



        road_layer.commitChanges()
        self.canvas.refresh()


        #uf.calculateIntersection(self.iface, cutter, tree_layer)




    def selectSelectedItem(self):

        remove_layer = ["Routes", "Buffer"]

        # remove selection on all layers
        layers = QgsMapLayerRegistry.instance().mapLayers().values()
        for layer in layers:

            try:
                layer.removeSelection()

            except:
                pass

            if layer.name() in remove_layer:
                QgsMapLayerRegistry.instance().removeMapLayers([layer])


        # determine active table

        if self.Pages.currentIndex() == 13:
            layer = uf.getLegendLayerByName(self.iface, "Shelters")
            self.table = self.table_shelter
            # coloumn of featureID
            col = 2

        elif self.Pages.currentIndex() == 14:
            self.table = self.table_hospital
            col = 2
            layer = uf.getLegendLayerByName(self.iface, "Hospitals")


        elif self.Pages.currentIndex() == 11:
            self.table = self.table_emergencies
            col = 6
            layer = uf.getLegendLayerByName(self.iface, "Emergencies")


        self.iface.setActiveLayer(layer)

        selectedItem = self.table.selectedItems()[0]
        row=selectedItem.row()

        featID = self.table.item(row, col).text()
        layer.select(int(featID))

        self.canvas.zoomToSelected()
        self.canvas.zoomByFactor(0.9)

        features = layer.selectedFeatures()
        self.nearestFeature(features[0].geometry().asPoint())







































