"""
Generates a 3-D heart atria model, suitable for attachment to the
3-D Heart Ventricles with Base 2.
"""

from __future__ import division
import math
from scaffoldmaker.annotation.annotationgroup import AnnotationGroup, findAnnotationGroupByName
from scaffoldmaker.utils.eft_utils import *
from scaffoldmaker.utils.geometry import *
from scaffoldmaker.utils.interpolation import *
from scaffoldmaker.utils.meshrefinement import MeshRefinement
from scaffoldmaker.utils.zinc_utils import *
from scaffoldmaker.utils.eftfactory_tricubichermite import eftfactory_tricubichermite
from opencmiss.zinc.element import Element, Elementbasis
from opencmiss.zinc.field import Field
from opencmiss.zinc.node import Node

class MeshType_3d_heartatria1(object):
    '''
    3-D heart atria model, suitable for attachment to the 3-D Heart Ventricles with Base 2.
    '''

    @staticmethod
    def getName():
        return '3D Heart Atria 1'

    @staticmethod
    def getDefaultOptions():
        return {
            'Number of elements around atrial free wall' : 8,
            'Number of elements around atrial septum' : 3,
            'Number of elements up atria' : 4,
            'Number of elements inlet' : 2,
            'Unit scale' : 1.0,
            'Atria base inner major axis length' : 0.55,
            'Atria base inner minor axis length' : 0.45,
            'Atria major axis rotation degrees' : 40.0,
            'Atria outer height' : 0.45,
            'Atrial septum thickness' : 0.07,
            'Atrial free wall thickness' : 0.02,
            'Atrial base wall thickness' : 0.07,
            'Atrial base slope degrees' : 30.0,
            'Aorta outer plus diameter' : 0.35,
            'Atrial base front incline degrees' : 15.0,
            'Atrial base back incline degrees' : 20.0,
            'Atrial base side incline degrees' : 20.0,
            'Atrial element size ratio anterior/posterior' : 1.5,
            'Number of left pulmonary veins' : 2,
            'Left pulmonary vein position up' : 0.6,
            'Left pulmonary vein angle up degrees' : 10.0,
            'Left pulmonary vein length factor' : 1.0,  # multiple of inner diameter that inlet center is away from atria wall
            'Left pulmonary vein inner diameter' : 0.11,
            'Left pulmonary vein wall thickness' : 0.009,
            'Number of right pulmonary veins' : 2,
            'Right pulmonary vein position up' : 0.85,
            'Right pulmonary vein angle up degrees' : 0.0,
            'Right pulmonary vein length factor' : 1.0,  # multiple of inner diameter that inlet center is away from atria wall
            'Right pulmonary vein inner diameter' : 0.12,
            'Right pulmonary vein wall thickness' : 0.009,
            'Inferior vena cava position up' : 0.3,
            'Inferior vena cava angle left degrees' : 0.0,
            'Inferior vena cava angle up degrees' : 10.0,
            'Inferior vena cava length factor' : 0.5,  # multiple of inner diameter that inlet center is away from atria wall
            'Inferior vena cava inner diameter' : 0.22,
            'Inferior vena cava wall thickness' : 0.015,
            'Superior vena cava position up' : 0.7,
            'Superior vena cava angle up degrees' : 20.0,
            'Superior vena cava length factor' : 0.5,  # multiple of inner diameter that inlet center is away from atria wall
            'Superior vena cava inner diameter' : 0.2,
            'Superior vena cava wall thickness' : 0.015,
            'Refine' : False,
            'Refine number of elements surface' : 4,
            'Refine number of elements through wall' : 1,
            'Use cross derivatives' : False,
        }

    @staticmethod
    def getOrderedOptionNames():
        return [
            'Number of elements around atrial free wall',
            'Number of elements around atrial septum',
            'Number of elements up atria',
            'Number of elements inlet',
            'Unit scale',
            'Atria base inner major axis length',
            'Atria base inner minor axis length',
            'Atria major axis rotation degrees',
            'Atria outer height',
            'Atrial septum thickness',
            'Atrial free wall thickness',
            'Atrial base wall thickness',
            'Atrial base slope degrees',
            'Aorta outer plus diameter',
            'Atrial base front incline degrees',
            'Atrial base back incline degrees',
            'Atrial base side incline degrees',
            'Atrial element size ratio anterior/posterior',
            'Number of left pulmonary veins',
            'Left pulmonary vein position up',
            'Left pulmonary vein angle up degrees',
            'Left pulmonary vein length factor',
            'Left pulmonary vein inner diameter',
            'Left pulmonary vein wall thickness',
            'Number of right pulmonary veins',
            'Right pulmonary vein position up',
            'Right pulmonary vein angle up degrees',
            'Right pulmonary vein length factor',
            'Right pulmonary vein inner diameter',
            'Right pulmonary vein wall thickness', 
            'Inferior vena cava position up',
            'Inferior vena cava angle up degrees',
            'Inferior vena cava angle left degrees',
            'Inferior vena cava length factor',
            'Inferior vena cava inner diameter',
            'Inferior vena cava wall thickness',
            'Superior vena cava position up',
            'Superior vena cava angle up degrees',
            'Superior vena cava length factor',
            'Superior vena cava inner diameter',
            'Superior vena cava wall thickness',
            'Refine',
            'Refine number of elements surface',
            'Refine number of elements through wall',
            #,'Use cross derivatives'
        ]

    @staticmethod
    def checkOptions(options):
        '''
        :return:  True if dependent options changed, otherwise False.
        '''
        dependentChanges = False
        if options['Number of elements around atrial free wall'] < 6:
            options['Number of elements around atrial free wall'] = 6
        # need even number of elements around free wall
        if (options['Number of elements around atrial free wall'] % 2) == 1:
            options['Number of elements around atrial free wall'] += 1
        if options['Number of elements around atrial septum'] < 2:
            options['Number of elements around atrial septum'] = 2
        if options['Number of elements up atria'] < 3:
            options['Number of elements up atria'] = 3
        if options['Number of elements inlet'] < 1:
            options['Number of elements inlet'] = 1
        for key in [
            'Unit scale',
            'Atria base inner major axis length',
            'Atria base inner minor axis length',
            'Atria outer height',
            'Atrial septum thickness',
            'Atrial free wall thickness',
            'Atrial base wall thickness',
            'Atrial base slope degrees',
            'Left pulmonary vein length factor',
            'Left pulmonary vein inner diameter',
            'Left pulmonary vein wall thickness',
            'Right pulmonary vein length factor',
            'Right pulmonary vein inner diameter',
            'Right pulmonary vein wall thickness',
            'Inferior vena cava length factor',
            'Inferior vena cava inner diameter',
            'Inferior vena cava wall thickness',
            'Superior vena cava length factor',
            'Superior vena cava inner diameter',
            'Superior vena cava wall thickness']:
            if options[key] < 0.0:
                options[key] = 0.0
        if options['Atrial element size ratio anterior/posterior'] < 0.1:
            options['Atrial element size ratio anterior/posterior'] = 0.1
        elif options['Atrial element size ratio anterior/posterior'] > 10.0:
            options['Atrial element size ratio anterior/posterior'] = 10.0
        for key in [
            'Number of left pulmonary veins',
            'Number of right pulmonary veins']:
            if options[key] < 1:
                options[key] = 1
            elif options[key] > 2:
                options[key] = 2
        for key in [
            'Left pulmonary vein position up',
            'Right pulmonary vein position up',
            'Inferior vena cava position up',
            'Superior vena cava position up']:
            if options[key] < 0.1:
                options[key] = 0.1
            elif options[key] > 0.9:
                options[key] = 0.9
        if options['Aorta outer plus diameter'] < options['Atrial septum thickness']:
            options['Aorta outer plus diameter'] = options['Atrial septum thickness']
        for key in [
            'Atria major axis rotation degrees']:
            if options[key] < -75.0:
                options[key] = -75.0
            elif options[key] > 75.0:
                options[key] = 75.0
        for key in [
            'Refine number of elements surface',
            'Refine number of elements through wall']:
            if options[key] < 1:
                options[key] = 1
        return dependentChanges

    @classmethod
    def generateBaseMesh(cls, region, options):
        """
        Generate the base tricubic Hermite mesh. See also generateMesh().
        :param region: Zinc region to define model in. Must be empty.
        :param options: Dict containing options. See getDefaultOptions().
        :return: list of AnnotationGroup
        """
        elementsCountAroundAtrialFreeWall = options['Number of elements around atrial free wall']
        elementsCountAroundAtrialSeptum = options['Number of elements around atrial septum']
        elementsCountAroundAtria = elementsCountAroundAtrialFreeWall + elementsCountAroundAtrialSeptum
        elementsCountUpAtria = options['Number of elements up atria']
        elementsCountInlet = options['Number of elements inlet']
        unitScale = options['Unit scale']

        aBaseInnerMajorMag = unitScale*0.5*options['Atria base inner major axis length']
        aBaseInnerMinorMag = unitScale*0.5*options['Atria base inner minor axis length']
        aMajorAxisRadians = math.radians(options['Atria major axis rotation degrees'])
        aOuterHeight = unitScale*options['Atria outer height']
        aortaOuterPlusRadius = unitScale*0.5*options['Aorta outer plus diameter']
        aBaseFrontInclineRadians = math.radians(options['Atrial base front incline degrees'])
        aBaseSideInclineRadians = math.radians(options['Atrial base side incline degrees'])
        aBaseBackInclineRadians = math.radians(options['Atrial base back incline degrees'])
        aElementSizeRatioAnteriorPosterior = options['Atrial element size ratio anterior/posterior']
        aSeptumThickness = unitScale*options['Atrial septum thickness']
        aFreeWallThickness = unitScale*options['Atrial free wall thickness']
        aBaseWallThickness = unitScale*options['Atrial base wall thickness']
        aBaseSlopeRadians = math.radians(options['Atrial base slope degrees'])
        lpvCount = options['Number of left pulmonary veins']
        lpvPositionUp = options['Left pulmonary vein position up']
        lpvAngleUpRadians = math.radians(options['Left pulmonary vein angle up degrees'])
        lpvLengthFactor = options['Left pulmonary vein length factor']
        lpvInnerRadius = unitScale*0.5*options['Left pulmonary vein inner diameter']
        lpvWallThickness = unitScale*options['Left pulmonary vein wall thickness']
        rpvCount = options['Number of right pulmonary veins']
        rpvPositionUp = options['Right pulmonary vein position up']
        rpvAngleUpRadians = math.radians(options['Right pulmonary vein angle up degrees'])
        rpvLengthFactor = options['Right pulmonary vein length factor']
        rpvInnerRadius = unitScale*0.5*options['Right pulmonary vein inner diameter']
        rpvWallThickness = unitScale*options['Right pulmonary vein wall thickness']
        ivcPositionUp = options['Inferior vena cava position up']
        ivcAngleUpRadians = math.radians(options['Inferior vena cava angle up degrees'])
        ivcAngleLeftRadians = math.radians(options['Inferior vena cava angle left degrees'])
        ivcLengthFactor = options['Inferior vena cava length factor']
        ivcInnerRadius = unitScale*0.5*options['Inferior vena cava inner diameter']
        ivcWallThickness = unitScale*options['Inferior vena cava wall thickness']
        svcPositionUp = options['Superior vena cava position up']
        svcAngleUpRadians = math.radians(options['Superior vena cava angle up degrees'])
        svcLengthFactor = options['Superior vena cava length factor']
        svcInnerRadius = unitScale*0.5*options['Superior vena cava inner diameter']
        svcWallThickness = unitScale*options['Superior vena cava wall thickness']
        useCrossDerivatives = options['Use cross derivatives']

        fm = region.getFieldmodule()
        fm.beginChange()
        coordinates = getOrCreateCoordinateField(fm)
        cache = fm.createFieldcache()

        laGroup = AnnotationGroup(region, 'left atrium', FMANumber = 7097, lyphID = 'Lyph ID unknown')
        raGroup = AnnotationGroup(region, 'right atrium', FMANumber = 7096, lyphID = 'Lyph ID unknown')
        aSeptumGroup = AnnotationGroup(region, 'interatrial septum', FMANumber = 7108, lyphID = 'Lyph ID unknown')
        fossaGroup = AnnotationGroup(region, 'fossa ovalis', FMANumber = 9246, lyphID = 'Lyph ID unknown')
        lipvGroup = AnnotationGroup(region, 'left inferior pulmonary vein', FMANumber = 49913, lyphID = 'Lyph ID unknown')
        lspvGroup = AnnotationGroup(region, 'left superior pulmonary vein', FMANumber = 49916, lyphID = 'Lyph ID unknown')
        ripvGroup = AnnotationGroup(region, 'right inferior pulmonary vein', FMANumber = 49911, lyphID = 'Lyph ID unknown')
        rspvGroup = AnnotationGroup(region, 'right superior pulmonary vein', FMANumber = 49914, lyphID = 'Lyph ID unknown')
        ivcInletGroup = AnnotationGroup(region, 'inferior vena cava inlet', FMANumber = 10951, lyphID = 'Lyph ID unknown')
        svcInletGroup = AnnotationGroup(region, 'superior vena cava inlet', FMANumber = 4720, lyphID = 'Lyph ID unknown')
        annotationGroups = [ laGroup, raGroup, aSeptumGroup, fossaGroup, lipvGroup, lspvGroup, ripvGroup, rspvGroup, ivcInletGroup, svcInletGroup ]
        # av boundary nodes are put in left and right fibrous ring groups only so they can be found by heart1
        lFibrousRingGroup = AnnotationGroup(region, 'left fibrous ring', FMANumber = 77124, lyphID = 'Lyph ID unknown')
        rFibrousRingGroup = AnnotationGroup(region, 'right fibrous ring', FMANumber = 77125, lyphID = 'Lyph ID unknown')

        ##############
        # Create nodes
        ##############

        nodes = fm.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)

        nodetemplate = nodes.createNodetemplate()
        nodetemplate.defineField(coordinates)
        nodetemplate.setValueNumberOfVersions(coordinates, -1, Node.VALUE_LABEL_VALUE, 1)
        nodetemplate.setValueNumberOfVersions(coordinates, -1, Node.VALUE_LABEL_D_DS1, 1)
        nodetemplate.setValueNumberOfVersions(coordinates, -1, Node.VALUE_LABEL_D_DS2, 1)
        nodetemplate.setValueNumberOfVersions(coordinates, -1, Node.VALUE_LABEL_D_DS3, 1)
        # LA/RA inlet elements are linear through the wall, hence their nodes do not have D_DS3 parameters
        nodetemplateLinearS3 = nodes.createNodetemplate()
        nodetemplateLinearS3.defineField(coordinates)
        nodetemplateLinearS3.setValueNumberOfVersions(coordinates, -1, Node.VALUE_LABEL_VALUE, 1)
        nodetemplateLinearS3.setValueNumberOfVersions(coordinates, -1, Node.VALUE_LABEL_D_DS1, 1)
        nodetemplateLinearS3.setValueNumberOfVersions(coordinates, -1, Node.VALUE_LABEL_D_DS2, 1)

        nodeIdentifier = max(1, getMaximumNodeIdentifier(nodes) + 1)

        aBaseSlopeHeight = aBaseWallThickness*math.sin(aBaseSlopeRadians)
        aBaseSlopeLength = aBaseWallThickness*math.cos(aBaseSlopeRadians)
        aBaseOuterMajorMag = aBaseInnerMajorMag + aBaseSlopeLength
        aBaseOuterMinorMag = aBaseInnerMinorMag + aBaseSlopeLength

        laCentre, laSeptumRadians, laBaseInnerx, laBaseInnerd1, laBaseInnerd2, laBaseOuterx, laBaseOuterd1, laBaseOuterd2 = \
            getLeftAtriumBasePoints(elementsCountAroundAtrialFreeWall, elementsCountAroundAtrialSeptum,
                aBaseInnerMajorMag, aBaseInnerMinorMag, aMajorAxisRadians,
                aBaseWallThickness, aBaseSlopeHeight, aBaseSlopeLength, aSeptumThickness,
                aortaOuterPlusRadius, aBaseFrontInclineRadians, aBaseSideInclineRadians, aBaseBackInclineRadians)

        laInnerx = [ laBaseInnerx ]
        laInnerd1 = [ laBaseInnerd1 ]
        laInnerd2 = [ laBaseInnerd2 ]
        laOuterx = [ laBaseOuterx ]
        laOuterd1 = [ laBaseOuterd1 ]
        laOuterd2 = [ laBaseOuterd2 ]
        laInnerd3 = [ [ None ]*elementsCountAroundAtria ]
        laOuterd3 = [ [ None ]*elementsCountAroundAtria ]
        for n2 in range(elementsCountUpAtria):
            for lav in (laInnerx, laInnerd1, laInnerd2, laInnerd3, laOuterx, laOuterd1, laOuterd2, laOuterd3):
                lav.append([ None ]*elementsCountAroundAtria)

        # GRC fudge factors:
        aOuterSeptumHeight = 0.85*aOuterHeight
        iaGrooveDerivative = 0.25*aSeptumThickness
        n1MidFreeWall = elementsCountAroundAtrialFreeWall//2
        elementsCountRidgeVenous = math.ceil(0.49*n1MidFreeWall)  # was 0.49
        elementsCountAroundEnd = elementsCountAroundAtrialFreeWall - 2*elementsCountRidgeVenous
        ridgeVenousDistance = 0.5*aSeptumThickness + 1.2*(ivcInnerRadius + svcInnerRadius + 2*(ivcWallThickness + svcWallThickness))

        # get ranges of nodes/elements to omit where inlets are

        elementsCountAcrossVC = elementsCountRidgeVenous
        elementsCountUpIVC = math.ceil(0.65*elementsCountUpAtria)
        elementsCountAroundIVC = (elementsCountAcrossVC + elementsCountUpIVC)*2
        ivce1min = 0
        ivce1max = ivce1min + elementsCountAcrossVC - 1
        ivce2min = 0
        ivce2max = ivce2min + elementsCountUpIVC - 1
        elementsCountUpSVC = math.ceil(0.58*elementsCountUpAtria)
        elementsCountAroundSVC = (elementsCountAcrossVC + elementsCountUpSVC)*2
        svce1max = elementsCountAroundAtrialFreeWall - 1
        svce1min = svce1max - elementsCountAcrossVC + 1
        svce2max = elementsCountUpAtria - 1
        svce2min = svce2max - elementsCountUpSVC + 1

        elementsCountUpLPV = math.ceil(0.66*elementsCountUpAtria)
        lipve2max = elementsCountUpAtria - 1
        lipve2min = lipve2max - elementsCountUpLPV + 1
        lspve2max = elementsCountUpAtria - 1
        lspve2min = lspve2max - elementsCountUpLPV + 1
        if lpvCount == 1:
            # merge inferior/superior lpv so straddles end ridge
            elementsCountAcrossLPV = elementsCountAroundEnd
            lspve1min = lipve1min = elementsCountAroundAtrialFreeWall//2 - elementsCountAcrossLPV//2
            lspve1max = lipve1max = lipve1min + elementsCountAcrossLPV - 1
        else:  # lpvCount == 2:
            elementsCountAcrossLPV = elementsCountAroundEnd//2
            lipve1min = elementsCountAroundAtrialFreeWall//2
            lipve1max = lipve1min + elementsCountAcrossLPV - 1
            lspve1max = elementsCountAroundAtrialFreeWall//2 - 1
            lspve1min = lspve1max - elementsCountAcrossLPV + 1
        elementsCountAroundLPV = elementsCountAcrossLPV + elementsCountUpLPV*2

        elementsCountAcrossRPV = elementsCountRidgeVenous  # was math.ceil(0.33*n1MidFreeWall)
        ripve1max = elementsCountAroundAtrialFreeWall - 1
        ripve1min = ripve1max - elementsCountAcrossRPV + 1
        rspve1min = 0
        rspve1max = rspve1min + elementsCountAcrossRPV - 1
        if rpvCount == 1:
            # merge inferior/superior rpv so straddles top ridge
            elementsCountUpRPV = math.ceil(0.66*elementsCountUpAtria)
            ripve2min = elementsCountUpAtria - (elementsCountUpRPV + 1)//2
            ripve2max = elementsCountUpAtria + elementsCountUpRPV//2 - 1
            rspve2min = elementsCountUpAtria*2 - ripve2max - 1
            rspve2max = elementsCountUpAtria*2 - ripve2min - 1
        else:  # rpvCount == 2:
            elementsCountUpRPV = math.ceil(0.49*elementsCountUpAtria)
            ripve2min = elementsCountUpAtria - elementsCountUpRPV
            ripve2max = elementsCountUpAtria - 1
            rspve2min = elementsCountUpAtria - elementsCountUpRPV
            rspve2max = elementsCountUpAtria - 1
        elementsCountAroundRPV = (elementsCountAcrossRPV + elementsCountUpRPV)*2

        addInlets = True

        # get la ridge points from cubic functions from ax = septum groove centre to cx at edge of venous atrium, using dx = mid outer LV base
        laSeptumBaseCentrex = [
            -0.5*aSeptumThickness,
            laCentre[1] + aBaseInnerMajorMag*math.sin(-aMajorAxisRadians)*math.cos(laSeptumRadians) \
                        + aBaseInnerMinorMag*math.cos(-aMajorAxisRadians)*math.sin(laSeptumRadians),
            -aBaseSlopeHeight ]
        ax = [ 0.0, laSeptumBaseCentrex[1], aOuterSeptumHeight ]
        ad1 = [ -iaGrooveDerivative, 0.0, 0.0 ]
        dx = laBaseOuterx[n1MidFreeWall]
        dd1 = [ -d for d in laBaseOuterd2[n1MidFreeWall]]
        # get point on venous peak
        # GRC fudge factor
        px, pd1 = sampleCubicHermiteCurves([ ax, dx ], [ ad1, dd1 ], elementsCountOut = 2, lengthFractionStart = 0.4, arcLengthDerivatives = True)[0:2]
        nx = [ ax, [ px[1][0], px[1][1], aOuterHeight ] ]
        nd1 = smoothCubicHermiteDerivativesLine(nx, [ ad1, [ pd1[1][0], pd1[1][1], 0.0 ] ], fixStartDerivative = True, fixEndDirection = True)
        ex = nx[1]
        ed1 = nd1[1]
        xi = 0.4
        # bx = in-between point to get more curvature near septum
        bx = interpolateCubicHermite(ax, ad1, ex, ed1, xi)
        bd1 = interpolateCubicHermiteDerivative(ax, ad1, ex, ed1, xi)
        # cx = limit of venous atrium on ridge
        cx, cd1, ce,  cxi= getCubicHermiteCurvesPointAtArcDistance([ ax, bx, ex, dx ], [ ad1, bd1, ed1, dd1 ], ridgeVenousDistance)
        if elementsCountRidgeVenous == 1:
            rx = [ [ ax[0], ax[1], ax[2] ], [ cx[0], cx[1], cx[2] ] ]
            rd1 = [ [ ad1[0], ad1[1], ad1[2] ], [ cd1[0], cd1[1], cd1[2] ] ]
        else:
            rx, rd1 = sampleCubicHermiteCurves([ ax, bx, cx ], [ ad1, bd1, cd1 ], elementsCountRidgeVenous,
                lengthFractionStart = 0.5, addLengthStart = 0.5*iaGrooveDerivative,
                arcLengthDerivatives = True)[0:2]

        # get points on outside arch of "venous" left atrium, anterior and posterior
        for na in range(elementsCountRidgeVenous + 1):
            np = elementsCountAroundAtrialFreeWall - na
            # sample arch from double cubic through anterior, ridge and posterior points
            lx, ld2, le, lxi = sampleCubicHermiteCurves(
                [ laBaseOuterx[na], rx[na], laBaseOuterx[np] ],
                [ laBaseOuterd2[na], [ -rd1[na][1], rd1[na][0], 0.0 ], [ -d for d in laBaseOuterd2[np]] ],
                2*elementsCountUpAtria, elementLengthStartEndRatio = aElementSizeRatioAnteriorPosterior,
                arcLengthDerivatives = True)[0:4]
            ld1 = interpolateSampleLinear([ laBaseOuterd1[na], rd1[na], [ -d for d in laBaseOuterd1[np]] ], le, lxi)

            for noa in range(1, elementsCountUpAtria*2):
                if noa <= elementsCountUpAtria:
                    laOuterx[noa][na] = lx[noa]
                    laOuterd1[noa][na] = ld1[noa]
                    laOuterd2[noa][na] = ld2[noa]
                else:
                    nop = elementsCountUpAtria*2 - noa
                    laOuterx[nop][np] = lx[noa]
                    laOuterd1[nop][np] = [ -d for d in ld1[noa] ]
                    laOuterd2[nop][np] = [ -d for d in ld2[noa] ]
            # fix scale of base derivative 2 on anterior and posterior
            laBaseOuterd2[na] = ld2[0]
            laBaseOuterd2[np] = [-d for d in ld2[2*elementsCountUpAtria] ]

        # add round quarter sphere in LA beyond "RA venous" zone
        # get apex point at end of "venous" atria
        vx  = laOuterx[elementsCountUpAtria][elementsCountRidgeVenous]
        vd1 = laOuterd2[elementsCountUpAtria][elementsCountRidgeVenous]
        vd2 = [ -d for d in laOuterd1[elementsCountUpAtria][elementsCountRidgeVenous] ]
        startDerivative1 = vector.magnitude(laBaseOuterd2[elementsCountRidgeVenous])
        startDerivative3 = vector.magnitude(laBaseOuterd2[elementsCountAroundAtrialFreeWall - elementsCountRidgeVenous])
        startDerivative2 = 0.666*startDerivative3  # GRC fudge factor
        radiansPerElementAroundEnd = math.pi/elementsCountAroundEnd
        for n in range(1, elementsCountAroundEnd):
            n1 = elementsCountRidgeVenous + n
            ax = laBaseOuterx[n1]
            ad1 = laBaseOuterd1[n1]
            ad2 = laBaseOuterd2[n1]
            radiansAround = n*radiansPerElementAroundEnd
            cosRadiansAround = math.cos(radiansAround)
            sinRadiansAround = math.sin(radiansAround)
            bx = vx
            bd1 = [ 0.5*(vd1[c]*sinRadiansAround - vd2[c]*cosRadiansAround) for c in range(3) ]
            bd2 = [ (vd1[c]*cosRadiansAround + vd2[c]*sinRadiansAround) for c in range(3) ]
            # quadratic Lagrange interpolation
            xi = radiansAround/math.pi
            phi1 = 1.0 + xi*(-3.0 + 2.0*xi)
            phi2 = 4*xi*(1.0 - xi)
            phi3 = xi*(-1.0 + 2.0*xi)
            startDerivative = phi1*startDerivative1 + phi2*startDerivative2 + phi3*startDerivative3
            endDerivative = vector.magnitude(bd2)
            ex, ed2, ee, exi = sampleCubicHermiteCurves([ ax, bx ], [ ad2, bd2 ], elementsCountUpAtria,
                addLengthStart = 0.5*startDerivative, lengthFractionStart = 0.5,
                addLengthEnd = 0.5*endDerivative, lengthFractionEnd = 0.5, arcLengthDerivatives = True)[0:4]
            ed1 = interpolateSampleLinear([ ad1, bd1 ], ee, exi)
            laOuterd2[0][n1] = ed2[0]
            for n2 in range(1, elementsCountUpAtria):
                laOuterx [n2][n1] = ex [n2]
                laOuterd1[n2][n1] = ed1[n2]
                laOuterd2[n2][n1] = ed2[n2]

        # smooth outer derivatives
        n1Limit = (elementsCountAroundAtrialFreeWall + 1)
        for n2 in range(1, elementsCountUpAtria):
            sd1 = smoothCubicHermiteDerivativesLine(laOuterx[n2][:n1Limit], laOuterd1[n2][:n1Limit], \
                fixStartDerivative = True, fixEndDerivative = True)
            for n1 in range(1, n1Limit - 1):
                laOuterd1[n2][n1] = sd1[n1]
        # top row:
        n2 = elementsCountUpAtria
        n1Limit = elementsCountRidgeVenous + 1
        nx = laOuterx[n2][:n1Limit]
        nx.append(laOuterx[n2 - 1][n1MidFreeWall])
        nd1 = laOuterd1[n2][:n1Limit]
        nd1.append([ -d for d in laOuterd2[n2 - 1][n1MidFreeWall] ])
        sd1 = smoothCubicHermiteDerivativesLine(nx, nd1, fixStartDerivative = True, fixEndDerivative = True)
        for n1 in range(1, n1Limit):
            laOuterd1[n2][n1] = sd1[n1]

        # get inner points
        for n2 in range(1, elementsCountUpAtria + 1):
            for n1 in range(elementsCountAroundAtria):
                ox = laOuterx[n2][n1]
                if ox is None:
                    continue
                od1 = laOuterd1[n2][n1]
                od2 = laOuterd2[n2][n1]
                unitRadial = vector.normalise(vector.crossproduct3(od1, od2))
                id3 = od3 = [ aFreeWallThickness*unitRadial[c] for c in range(3) ]
                laInnerd3[n2][n1] = laOuterd3[n2][n1] = od3
                ix = laInnerx[n2][n1]
                if ix is not None:
                    continue
                ix = [ (ox[c] - od3[c]) for c in range(3) ]

                # calculate inner d1 from curvature around
                curvature = 0.0
                count = 0
                if (n1 < elementsCountAroundAtrialFreeWall) and (laOuterx[n2][n1 + 1] is not None):
                    curvature -= getCubicHermiteCurvature(laOuterx[n2][n1], laOuterd1[n2][n1], laOuterx[n2][n1 + 1], laOuterd1[n2][n1 + 1], unitRadial, 0.0)
                    count += 1
                if (n1 > 0) and (laOuterx[n2][n1 - 1] is not None):
                    curvature -= getCubicHermiteCurvature(laOuterx[n2][n1 - 1], laOuterd1[n2][n1 - 1], laOuterx[n2][n1], laOuterd1[n2][n1], unitRadial, 1.0)
                    count += 1
                curvature /= count
                factor = 1.0 - curvature*aFreeWallThickness
                id1 = [ factor*c for c in od1 ]

                # calculate inner d2 from curvature up
                curvature = 0.0
                count = 0
                if (n2 < elementsCountUpAtria) and (laOuterx[n2 + 1][n1] is not None):
                    curvature -= getCubicHermiteCurvature(laOuterx[n2][n1], laOuterd2[n2][n1], laOuterx[n2 + 1][n1], laOuterd2[n2 + 1][n1], unitRadial, 0.0)
                    count += 1
                if n2 > 0:
                    curvature -= getCubicHermiteCurvature(laOuterx[n2 - 1][n1], laOuterd2[n2 - 1][n1], laOuterx[n2][n1], laOuterd2[n2][n1], unitRadial, 1.0)
                    count += 1
                curvature /= count
                factor = 1.0 - curvature*aFreeWallThickness
                id2 = [ factor*c for c in od2 ]

                laInnerx[n2][n1] = ix
                laInnerd1[n2][n1] = id1
                laInnerd2[n2][n1] = id2
                laInnerd3[n2][n1] = id3

        # fix inner base derivative 2 to fit incline
        for n1 in range(1, elementsCountAroundAtrialFreeWall + 1):
            d2 = interpolateHermiteLagrangeDerivative(laInnerx[1][n1], [ -d for d in laInnerd2[1][n1] ], laInnerx[0][n1], 1.0)
            laInnerd2[0][n1] = [ -d for d in d2 ]
        # special fix inner base derivative 2 at cfb = slope of cfbLeft inner derivative 2
        laInnerd2[0][0] = laInnerd2[0][1]

        # calculate fossa positions early to use in smoothing septum
        # GRC the following 4 variables could be made into options
        fossaCentreY = laSeptumBaseCentrex[1]
        fossaCentreZ = 0.5*aOuterSeptumHeight
        # fossa width is based on distance from cfb to fossa centre
        fossaMagY = (laBaseOuterx[0][1] - fossaCentreY)*0.36
        fossaMagZ = 0.2*aOuterSeptumHeight

        ux = [ laSeptumBaseCentrex[0], fossaCentreY, fossaCentreZ ]
        ud1 = [ 0.0, fossaMagY, 0.0 ]
        ud2 = [ 0.0, 0.0, fossaMagZ]
        gx  = laInnerx [elementsCountUpAtria][1]
        gd1 = laInnerd1[elementsCountUpAtria][1]
        gd2 = laInnerd2[elementsCountUpAtria][1]
        gd3 = laInnerd3[elementsCountUpAtria][1]
        fradians = math.atan2(gx[2] - ux[2], gx[1] - ux[1])
        fd1 = [ ( ud1[c]*math.cos(fradians) + ud2[c]*math.sin(fradians)) for c in range(3) ]
        fd2 = [ (-ud1[c]*math.sin(fradians) + ud2[c]*math.cos(fradians)) for c in range(3) ]
        fx = [ (ux[c] + fd1[c]) for c in range(3) ]
        tx, td1, te, txi = sampleCubicHermiteCurves([ fx, gx ], [ fd1, gd1 ], elementsCountOut = 2,
            addLengthStart = 0.5*vector.magnitude(fd1), lengthFractionStart = 0.5,
            addLengthEnd = 0.5*vector.magnitude(gd1), lengthFractionEnd = 0.5, arcLengthDerivatives = True)[0:4]
        td2 = interpolateSampleLinear([ fd2, gd2 ], te, txi)
        mx  = tx [1]
        md1 = td1[1]
        md2 = td2[1]

        if False:
            node = nodes.createNode(nodeIdentifier, nodetemplate)
            cache.setNode(node)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_VALUE, 1, fx )
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS1, 1, fd1)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS2, 1, fd2)
            nodeIdentifier += 1

            node = nodes.createNode(nodeIdentifier, nodetemplate)
            cache.setNode(node)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_VALUE, 1, gx )
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS1, 1, gd1)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS2, 1, gd2)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS3, 1, gd3)
            nodeIdentifier += 1

        # fix inner nodes near septum to thicken wall and transition to septum
        ax  = laInnerx [0][0]
        ad1 = laInnerd1[0][0]
        ad2 = laInnerd2[0][0]
        # get start distance to account for aBaseSlopeRadians
        scale2 = aBaseSlopeHeight/ad2[2]
        addLengthStart = vector.magnitude([ ad2[0]*scale2, ad2[1]*scale2, aBaseSlopeHeight ])
        px  = laInnerx [0][elementsCountAroundAtrialFreeWall]
        pd1 = [ -d for d in laInnerd1[0][elementsCountAroundAtrialFreeWall] ]
        pd2 = [ -d for d in laInnerd2[0][elementsCountAroundAtrialFreeWall] ]
        # make steeper and with low x component
        ad2 = [ 0.5*ad2[0], ad2[1], 1.5*ad2[2] ]
        pd2 = [ 0.5*pd2[0], pd2[1], 1.5*pd2[2] ]
        # get start distance to account for aBaseSlopeRadians
        scale2 = -aBaseSlopeHeight/pd2[2]
        addLengthEnd = vector.magnitude([ pd2[0]*scale2, pd2[1]*scale2, aBaseSlopeHeight ])
        ix, id2, ie, ixi = sampleCubicHermiteCurves([ ax , mx , px  ], [ ad2, md2, pd2 ], 2*elementsCountUpAtria,
            addLengthStart, addLengthEnd, elementLengthStartEndRatio = aElementSizeRatioAnteriorPosterior, arcLengthDerivatives = True)[0:4]
        id1 = interpolateSampleLinear([ ad1, md1, pd1 ], ie, ixi)
        for noa in range(elementsCountUpAtria*2 + 1):
            nop = elementsCountUpAtria*2 - noa
            if noa <= elementsCountUpAtria:
                laInnerx[noa][0] = ix[noa]
                laInnerd1[noa][0] = id1[noa]
                laInnerd2[noa][0] = id2[noa]
            else:
                laInnerx[nop][elementsCountAroundAtrialFreeWall] = ix[noa]
                laInnerd1[nop][elementsCountAroundAtrialFreeWall] = [ -d for d in id1[noa] ]
                laInnerd2[nop][elementsCountAroundAtrialFreeWall] = [ -d for d in id2[noa] ]

        # fix derivative 3 through wall
        n2 = 0
        for n1 in range(elementsCountAroundAtrialFreeWall + 1, elementsCountAroundAtria):
            laInnerd3[n2][n1] = [ -2.0*laBaseInnerx[n1][0], 0.0, 0.0 ]
        for n2 in range(elementsCountUpAtria + 1):
            n1Limit = n1MidFreeWall if (n2 == elementsCountUpAtria) else (elementsCountAroundAtrialFreeWall + 1)
            for n1 in range(n1Limit):
                if laOuterx[n2][n1] is None:
                    continue
                laInnerd3[n2][n1] = laOuterd3[n2][n1] = [ (laOuterx[n2][n1][c] - laInnerx[n2][n1][c]) for c in range(3) ]
        # fix cfb-interatrial groove-crux centre derivative 3:
        for n2 in range(elementsCountUpAtria + 1):
            laOuterd3[n2][0] = [ 0.0, laOuterx[n2][0][1] - laInnerx[n2][0][1], laOuterx[n2][0][2] - laInnerx[n2][0][2] ]
        for n2 in range(elementsCountUpAtria):
            laOuterd3[n2][elementsCountAroundAtrialFreeWall] = [ 0.0,
                laOuterx[n2][elementsCountAroundAtrialFreeWall][1] - laInnerx[n2][elementsCountAroundAtrialFreeWall][1],
                laOuterx[n2][elementsCountAroundAtrialFreeWall][2] - laInnerx[n2][elementsCountAroundAtrialFreeWall][2] ]

        # fossa ovalis points at centre and around
        elementsCountFossaBaseCentre = max(elementsCountAroundAtrialSeptum - 2, 1)
        elementsCountFossaBase = 2 + elementsCountFossaBaseCentre
        elementsCountAroundFossa = elementsCountFossaBaseCentre + 2*(elementsCountUpAtria - 1)
        fossaPerimeterLength = getApproximateEllipsePerimeter(fossaMagY, fossaMagZ)
        # allow more space for fossa base elements
        elementSizeAroundFossa = fossaPerimeterLength/(elementsCountAroundFossa + 1)
        elementSizeAroundFossaBase = (elementSizeAroundFossa*elementsCountFossaBase)/(elementsCountFossaBase - 1)
        elementSizeAroundFossaTransition = 0.5*(elementSizeAroundFossa + elementSizeAroundFossaBase)

        radiansAround = updateEllipseAngleByArcLength(fossaMagY, fossaMagZ, fradians - math.pi, -0.5*elementsCountFossaBaseCentre*elementSizeAroundFossaBase)
        fossaRadiansAround = []
        fossaDerivativesAround = []
        for nf in range(elementsCountAroundFossa):
            fossaRadiansAround.append(radiansAround)
            fossaDerivativesAround.append(elementSizeAroundFossaBase if (nf <= elementsCountFossaBaseCentre) else elementSizeAroundFossa)
            radiansAround = updateEllipseAngleByArcLength(fossaMagY, fossaMagZ, radiansAround, \
                elementSizeAroundFossaBase if (nf < elementsCountFossaBaseCentre) \
                else (elementSizeAroundFossa if (nf > (elementsCountFossaBaseCentre))
                else elementSizeAroundFossaTransition))
        fossaCentrex = []
        fossaCentred1 = []
        fossaCentred2 = []
        fossaCentred3 = []
        fossax = [ [], [] ]
        fossad1 = [ [], [] ]
        fossad2 = [ [], [] ]
        fossad3 = [ [], [] ]
        septumd3 = [ aSeptumThickness, 0.0, 0.0 ]
        for n3 in range(2):
            fossaCentrex.append([ aSeptumThickness*(-0.5 if (n3 == 0) else 0.5), fossaCentreY, fossaCentreZ ])
            fossaCentred1.append([ 0.0, fossaMagY, 0.0 ])
            fossaCentred2.append([ 0.0, 0.0, fossaMagZ ])
            fossaCentred3.append(septumd3)
            for nf in range(elementsCountAroundFossa):
                radiansAround = fossaRadiansAround[nf]
                cosRadiansAround = math.cos(radiansAround)
                sinRadiansAround = math.sin(radiansAround)
                fossax[n3].append([ fossaCentrex[n3][0], fossaCentreY + fossaMagY*cosRadiansAround, fossaCentreZ + fossaMagZ*sinRadiansAround ])
                fossad1[n3].append(vector.setMagnitude([ 0.0, -fossaMagY*sinRadiansAround, fossaMagZ*cosRadiansAround ], fossaDerivativesAround[nf]))
                fossad2[n3].append([ 0.0, -fossaMagY*cosRadiansAround, -fossaMagZ*sinRadiansAround ])
                fossad3[n3].append(septumd3)

        # calculate base septum derivative 2 to smoothly connect to adjacent fossa nodes
        if elementsCountAroundAtrialSeptum == 2:
            laInnerd2[0][elementsCountAroundAtrialFreeWall + 1] = [ 0.0, 0.0, 2.0*(fossaCentreZ - fossaMagZ + aBaseSlopeHeight) - fossaMagZ ]
        else:
            for ns in range(1, elementsCountAroundAtrialSeptum):
                x1 = laInnerx[0][elementsCountAroundAtrialFreeWall + ns]
                x2 = fossax[0][ns - 1]
                d2 = fossad2[0][ns - 1]
                if ns == 1:
                    d2 = [ (d2[c] - fossad1[0][ns - 1][c]) for c in range(3) ]
                elif ns == (elementsCountAroundAtrialSeptum - 1):
                    d2 = [ (d2[c] + fossad1[0][ns - 1][c]) for c in range(3) ]
                laInnerd2[0][elementsCountAroundAtrialFreeWall + ns] = interpolateLagrangeHermiteDerivative(x1, x2, d2, 0.0)

        # Create nodes around atria
        pvEdgeDerivativeFactor1 = 0.50   # GRC fudge factor: factor reducing derivatives between pvs
        pvEdgeDerivativeFactor2 = 0.666  # GRC fudge factor: factor reducing derivatives beneath lpv
        laNodeId = [ [], [] ]
        raNodeId = [ [], [] ]
        ran1FreeWallStart = elementsCountAroundAtrialSeptum - 1
        ran1MidFreeWall = ran1FreeWallStart + n1MidFreeWall
        for n3 in range(2):
            for n2 in range(elementsCountUpAtria + 1):
                if n3 == 0:
                    lax = laInnerx[n2]
                    lad1 = laInnerd1[n2]
                    lad2 = laInnerd2[n2]
                    lad3 = laInnerd3[n2]
                else:
                    lax =  laOuterx[n2]
                    lad1 = laOuterd1[n2]
                    lad2 = laOuterd2[n2]
                    lad3 = laOuterd3[n2]

                # left atrium
                aNodeId = [ None ]*elementsCountAroundAtria
                for n1 in range(elementsCountAroundAtria):
                    if (n2 == elementsCountUpAtria) and (n1 > elementsCountRidgeVenous) and (n1 <= elementsCountAroundAtrialFreeWall):
                        if (n1 < (elementsCountAroundAtrialFreeWall - elementsCountRidgeVenous)):
                            aNodeId[n1] = aNodeId[elementsCountRidgeVenous]
                        else:
                            aNodeId[n1] = aNodeId[elementsCountAroundAtrialFreeWall - n1]
                        continue
                    if lax[n1] is None:
                        continue
                    if addInlets:
                        if (n1 > lipve1min) and (n1 <= lipve1max) and (n2 > lipve2min) and (n2 <= lipve2max):
                            continue  # lipv inlet location
                        if (n1 > lspve1min) and (n1 <= lspve1max) and (n2 > lspve2min) and (n2 <= lspve2max):
                            continue  # lspv inlet location
                        if (n1 > ripve1min) and (n1 <= ripve1max) and (n2 > ripve2min) and (n2 <= ripve2max):
                            continue  # ripv inlet location
                        if (n1 > rspve1min) and (n1 <= rspve1max) and (n2 > rspve2min) and (n2 <= rspve2max):
                            continue  # rspv inlet location
                    node = nodes.createNode(nodeIdentifier, nodetemplate)
                    aNodeId[n1] = nodeIdentifier
                    cache.setNode(node)
                    coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_VALUE, 1, lax[n1])
                    # reduce edge derivative between and below LPV inlets to better fit them:
                    if (n1 == n1MidFreeWall) and (n2 > lipve2min):
                        coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS1, 1, [ pvEdgeDerivativeFactor1*d for d in lad1[n1]])
                    else:
                        coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS1, 1, lad1[n1])
                    if (n2 == elementsCountUpAtria) and (n1 < elementsCountRidgeVenous):
                        coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS2, 1, [ pvEdgeDerivativeFactor1*d for d in lad2[n1]])
                    #elif (n2 == lipve2min) and (n1 > lspve1min) and (n1 <= lipve1max):
                    #    coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS2, 1, [ pvEdgeDerivativeFactor2*d for d in lad2[n1]])
                    else:
                        coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS2, 1, lad2[n1])
                    coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS3, 1, lad3[n1])
                    nodeIdentifier += 1
                laNodeId[n3].append(aNodeId)

                # right atrium
                aNodeId = [ None ]*elementsCountAroundAtria
                for n1 in range(elementsCountAroundAtria):
                    n1l = elementsCountAroundAtria - 1 - n1
                    if (n3 == 1) and ((n1l == 0) or (n1l == elementsCountAroundAtrialFreeWall)):
                        aNodeId[n1] = laNodeId[n3][n2][n1l]
                        continue
                    if (n2 == elementsCountUpAtria) and (n1l > elementsCountRidgeVenous) and (n1l <= elementsCountAroundAtrialFreeWall):
                        continue  # copy from anterior, below, once created
                    if lax[n1l] is None:
                        continue
                    if addInlets:
                        if (n1 > (ran1FreeWallStart + ivce1min)) and (n1 <= (ran1FreeWallStart + ivce1max)) and (n2 > ivce2min) and (n2 <= ivce2max):
                            continue  # ivc inlet location
                        if (n1 > (ran1FreeWallStart + svce1min)) and (n1 <= (ran1FreeWallStart + svce1max)) and (n2 > svce2min) and (n2 <= svce2max):
                            continue  # svc inlet location
                    node = nodes.createNode(nodeIdentifier, nodetemplate)
                    aNodeId[n1] = nodeIdentifier
                    cache.setNode(node)
                    coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_VALUE, 1, [  -lax[n1l][0],   lax[n1l][1],   lax[n1l][2] ])
                    coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS1, 1, [  lad1[n1l][0], -lad1[n1l][1], -lad1[n1l][2] ])
                    coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS2, 1, [ -lad2[n1l][0],  lad2[n1l][1],  lad2[n1l][2] ])
                    coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS3, 1, [ -lad3[n1l][0],  lad3[n1l][1],  lad3[n1l][2] ])
                    nodeIdentifier += 1
                if n2 == elementsCountUpAtria:
                    # fix up posterior ridge and end nodes
                    for n1 in range(ran1FreeWallStart, ran1FreeWallStart + elementsCountRidgeVenous + 1):
                        aNodeId[n1] = aNodeId[elementsCountAroundAtria + ran1FreeWallStart - n1 - 1]
                    for n1 in range(ran1FreeWallStart + elementsCountRidgeVenous + 1, ran1FreeWallStart + elementsCountAroundAtrialFreeWall - elementsCountRidgeVenous):
                        aNodeId[n1] = aNodeId[ran1FreeWallStart + elementsCountRidgeVenous]
                raNodeId[n3].append(aNodeId)

        # add nodes to left/right fibrous ring groups so heart1 can find them
        for i in range(2):
            fibrousRingGroup = lFibrousRingGroup if (i == 0) else rFibrousRingGroup
            fibrousRingNodesetGroup = fibrousRingGroup.getNodesetGroup(nodes)
            for n3 in range(2):
                aNodeId = laNodeId[n3][0] if (i == 0) else raNodeId[n3][0]
                for n1 in range(elementsCountAroundAtria):
                    if aNodeId[n1]:
                        node = nodes.findNodeByIdentifier(aNodeId[n1])
                        fibrousRingNodesetGroup.addNode(node)

        # create fossa ovalis nodes
        fossaCentreNodeId = []
        fossaNodeId = [ [], [] ]
        for n3 in range(2):
            node = nodes.createNode(nodeIdentifier, nodetemplate)
            cache.setNode(node)
            result = coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_VALUE, 1, fossaCentrex[n3])
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS1, 1, fossaCentred1[n3])
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS2, 1, fossaCentred2[n3])
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS3, 1, fossaCentred3[n3])
            fossaCentreNodeId.append(nodeIdentifier)
            nodeIdentifier += 1
            for nf in range(elementsCountAroundFossa):
                node = nodes.createNode(nodeIdentifier, nodetemplate)
                cache.setNode(node)
                result = coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_VALUE, 1, fossax[n3][nf])
                coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS1, 1, fossad1[n3][nf])
                coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS2, 1, fossad2[n3][nf])
                coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS3, 1, fossad3[n3][nf])
                fossaNodeId[n3].append(nodeIdentifier)
                nodeIdentifier += 1

        #################
        # Create elements
        #################

        mesh = fm.findMeshByDimension(3)

        elementIdentifier = max(1, getMaximumElementIdentifier(mesh) + 1)

        laMeshGroup = laGroup.getMeshGroup(mesh)
        raMeshGroup = raGroup.getMeshGroup(mesh)
        aSeptumMeshGroup = aSeptumGroup.getMeshGroup(mesh)
        fossaMeshGroup = fossaGroup.getMeshGroup(mesh)
        lipvMeshGroup = lipvGroup.getMeshGroup(mesh)
        lspvMeshGroup = lspvGroup.getMeshGroup(mesh)
        ripvMeshGroup = ripvGroup.getMeshGroup(mesh)
        rspvMeshGroup = rspvGroup.getMeshGroup(mesh)
        ivcInletMeshGroup = ivcInletGroup.getMeshGroup(mesh)
        svcInletMeshGroup = svcInletGroup.getMeshGroup(mesh)

        tricubichermite = eftfactory_tricubichermite(mesh, useCrossDerivatives)
        tricubicHermiteBasis = fm.createElementbasis(3, Elementbasis.FUNCTION_TYPE_CUBIC_HERMITE)

        eft = tricubichermite.createEftBasic()
        elementtemplate = mesh.createElementtemplate()
        elementtemplate.setElementShapeType(Element.SHAPE_TYPE_CUBE)
        elementtemplate.defineField(coordinates, -1, eft)

        elementtemplateX = mesh.createElementtemplate()
        elementtemplateX.setElementShapeType(Element.SHAPE_TYPE_CUBE)

        # create outside wall elements

        for e2 in range(elementsCountUpAtria):

            # left atrium, starting at cfb / anterior interatrial sulcus
            for e1 in range(-1, elementsCountAroundAtrialFreeWall):
                eft1 = eft
                elementtemplate1 = elementtemplate
                nids = [
                    laNodeId[0][e2][e1], laNodeId[0][e2][e1 + 1], laNodeId[0][e2 + 1][e1], laNodeId[0][e2 + 1][e1 + 1],
                    laNodeId[1][e2][e1], laNodeId[1][e2][e1 + 1], laNodeId[1][e2 + 1][e1], laNodeId[1][e2 + 1][e1 + 1]]
                scalefactors = None
                meshGroups = [ laMeshGroup ]

                if addInlets:
                    if (e1 >= lipve1min) and (e1 <= lipve1max) and (e2 >= lipve2min) and (e2 <= lipve2max):
                        continue  # lipv inlet location
                    if (e1 >= lspve1min) and (e1 <= lspve1max) and (e2 >= lspve2min) and (e2 <= lspve2max):
                        continue  # lspv inlet location
                    if (e1 >= ripve1min) and (e1 <= ripve1max) and (e2 >= ripve2min) and (e2 <= ripve2max):
                        continue  # ripv inlet location
                    if (e1 >= rspve1min) and (e1 <= rspve1max) and (e2 >= rspve2min) and (e2 <= rspve2max):
                        continue  # rspv inlet location
                if e1 == -1:
                    # cfb/anterior interatrial groove straddles left and right atria, collapsed to 6 node wedge
                    nids[0] = raNodeId[0][e2][-1]
                    nids[2] = raNodeId[0][e2 + 1][-1]
                    nids.pop(6)
                    nids.pop(4)
                    meshGroups += [ raMeshGroup ]
                    eft1 = tricubichermite.createEftNoCrossDerivatives()
                    setEftScaleFactorIds(eft1, [1], [])
                    remapEftNodeValueLabel(eft1, [ 1, 3 ], Node.VALUE_LABEL_D_DS1, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS3, [] ) ])
                    remapEftNodeValueLabel(eft1, [ 2, 4 ], Node.VALUE_LABEL_D_DS1, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS3, [1] ) ])
                    remapEftNodeValueLabel(eft1, [ 5, 6, 7, 8 ], Node.VALUE_LABEL_D_DS1, [])
                    remapEftNodeValueLabel(eft1, [ 5, 7 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS3, []) ])
                    remapEftNodeValueLabel(eft1, [ 6, 8 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [1] ), ( Node.VALUE_LABEL_D_DS3, []) ])
                    ln_map = [ 1, 2, 3, 4, 5, 5, 6, 6 ]
                    remapEftLocalNodes(eft1, 6, ln_map)
                elif e1 == 0:
                    # general linear map d3 adjacent to collapsed cfb
                    eft1 = tricubichermite.createEftNoCrossDerivatives()
                    setEftScaleFactorIds(eft1, [1], [])
                    remapEftNodeValueLabel(eft1, [ 5, 7 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [1] ), ( Node.VALUE_LABEL_D_DS3, []) ])
                elif e1 == (elementsCountAroundAtrialFreeWall - 1):
                    # general linear map d3 adjacent to collapsed crux
                    eft1 = tricubichermite.createEftNoCrossDerivatives()
                    if e2 == (elementsCountUpAtria - 1):
                        # reverse d1 and d2 on ridge
                        setEftScaleFactorIds(eft1, [1], [])
                        scaleEftNodeValueLabels(eft1, [ 3, 4, 7, 8 ], [ Node.VALUE_LABEL_D_DS1, Node.VALUE_LABEL_D_DS2 ], [ 1 ])
                        remapEftNodeValueLabel(eft1, [ 6 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS3, []) ])
                        remapEftNodeValueLabel(eft1, [ 8 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [1] ), ( Node.VALUE_LABEL_D_DS3, []) ])
                    else:
                        remapEftNodeValueLabel(eft1, [ 6, 8 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS3, []) ])
                elif (e2 == (elementsCountUpAtria - 1)) and (e1 >= elementsCountRidgeVenous) and \
                        (e1 < (elementsCountAroundAtrialFreeWall - elementsCountRidgeVenous)):
                    # 6 node pole elements
                    nids.pop(7)
                    nids.pop(3)
                    s = e1 - elementsCountRidgeVenous
                    radiansAround0 = 0.5*math.pi + s*radiansPerElementAroundEnd
                    radiansAround1 = radiansAround0 + radiansPerElementAroundEnd
                    # scale factor identifiers follow convention of offsetting by 100 for each 'version'
                    eft1 = tricubichermite.createEftShellPoleTop(s*100, (s + 1)*100)
                    scalefactors = [
                        -1.0,
                        math.cos(radiansAround0), math.sin(radiansAround0), radiansPerElementAroundEnd,
                        math.cos(radiansAround1), math.sin(radiansAround1), radiansPerElementAroundEnd,
                        math.cos(radiansAround0), math.sin(radiansAround0), radiansPerElementAroundEnd,
                        math.cos(radiansAround1), math.sin(radiansAround1), radiansPerElementAroundEnd
                    ]
                elif (e2 == (elementsCountUpAtria - 1)) and (e1 > (elementsCountAroundAtrialFreeWall//2)):
                    # reverse d1 and d2 on ridge
                    eft1 = tricubichermite.createEftNoCrossDerivatives()
                    setEftScaleFactorIds(eft1, [1], [])
                    scaleEftNodeValueLabels(eft1, [ 3, 4, 7, 8 ], [ Node.VALUE_LABEL_D_DS1, Node.VALUE_LABEL_D_DS2 ], [ 1 ])

                if eft1 is not eft:
                    elementtemplateX.defineField(coordinates, -1, eft1)
                    elementtemplate1 = elementtemplateX

                element = mesh.createElement(elementIdentifier, elementtemplate1)
                result2 = element.setNodesByIdentifier(eft1, nids)
                if scalefactors:
                    result3 = element.setScaleFactors(eft1, scalefactors)
                elif eft1.getNumberOfLocalScaleFactors() == 1:
                    result3 = element.setScaleFactors(eft1, [ -1.0 ])
                else:
                    result3 = ' '
                #print('create element la', element.isValid(), elementIdentifier, result2, result3, nids)
                elementIdentifier += 1

                for meshGroup in meshGroups:
                    meshGroup.addElement(element)

            # right atrium, starting at crux / posterior interatrial sulcus
            for e1 in range(-1, elementsCountAroundAtrialFreeWall):
                n1 = ran1FreeWallStart + e1
                eft1 = eft
                elementtemplate1 = elementtemplate
                nids = [
                    raNodeId[0][e2][n1], raNodeId[0][e2][n1 + 1], raNodeId[0][e2 + 1][n1], raNodeId[0][e2 + 1][n1 + 1],
                    raNodeId[1][e2][n1], raNodeId[1][e2][n1 + 1], raNodeId[1][e2 + 1][n1], raNodeId[1][e2 + 1][n1 + 1]]
                scalefactors = None
                meshGroups = [ raMeshGroup ]

                if addInlets:
                    if (e1 >= ivce1min) and (e1 <= ivce1max) and (e2 >= ivce2min) and (e2 <= ivce2max):
                        continue  # ivc inlet location
                    if (e1 >= svce1min) and (e1 <= svce1max) and (e2 >= svce2min) and (e2 <= svce2max):
                        continue  # svc inlet location
                if e1 == -1:
                    # crux/posterior interatrial groove straddles left and right atria, collapsed to 6 node wedge
                    nids[0] = laNodeId[0][e2][elementsCountAroundAtrialFreeWall]
                    nids[2] = laNodeId[0][e2 + 1][elementsCountAroundAtrialFreeWall]
                    nids.pop(6)
                    nids.pop(4)
                    meshGroups += [ laMeshGroup ]
                    eft1 = tricubichermite.createEftNoCrossDerivatives()
                    setEftScaleFactorIds(eft1, [1], [])
                    remapEftNodeValueLabel(eft1, [ 1, 3 ], Node.VALUE_LABEL_D_DS1, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS3, [] ) ])
                    remapEftNodeValueLabel(eft1, [ 2, 4 ], Node.VALUE_LABEL_D_DS1, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS3, [1] ) ])
                    remapEftNodeValueLabel(eft1, [ 5, 6, 7, 8 ], Node.VALUE_LABEL_D_DS1, [])
                    remapEftNodeValueLabel(eft1, [ 5, 7 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS3, []) ])
                    if e2 == (elementsCountUpAtria - 1):
                        # reverse D_DS1, D_DS2 on ridge, avoiding scaling D_DS1 by -1 twice at node 8
                        scaleEftNodeValueLabels(eft1, [ 3, 4, 7 ], [ Node.VALUE_LABEL_D_DS1, Node.VALUE_LABEL_D_DS2 ], [ 1 ])
                        scaleEftNodeValueLabels(eft1, [ 8 ], [ Node.VALUE_LABEL_D_DS2 ], [ 1 ])
                        remapEftNodeValueLabel(eft1, [ 6 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [1] ), ( Node.VALUE_LABEL_D_DS3, []) ])
                        remapEftNodeValueLabel(eft1, [ 8 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS3, []) ])
                    else:
                        remapEftNodeValueLabel(eft1, [ 6, 8 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [1] ), ( Node.VALUE_LABEL_D_DS3, []) ])
                    ln_map = [ 1, 2, 3, 4, 5, 5, 6, 6 ]
                    remapEftLocalNodes(eft1, 6, ln_map)
                elif e1 == 0:
                    # general linear map d3 adjacent to collapsed crux
                    eft1 = tricubichermite.createEftNoCrossDerivatives()
                    setEftScaleFactorIds(eft1, [1], [])
                    if e2 == (elementsCountUpAtria - 1):
                        # reverse d1 and d2 on ridge, avoiding scaling D_DS1 by -1 twice at node 7
                        setEftScaleFactorIds(eft1, [1], [])
                        scaleEftNodeValueLabels(eft1, [ 3, 4, 7, 8 ], [ Node.VALUE_LABEL_D_DS1, Node.VALUE_LABEL_D_DS2 ], [ 1 ])
                        remapEftNodeValueLabel(eft1, [ 5 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [1] ), ( Node.VALUE_LABEL_D_DS3, []) ])
                        remapEftNodeValueLabel(eft1, [ 7 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS3, []) ])
                    else:
                        remapEftNodeValueLabel(eft1, [ 5, 7 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [1] ), ( Node.VALUE_LABEL_D_DS3, []) ])
                elif e1 == (elementsCountAroundAtrialFreeWall - 1):
                    # general linear map d3 adjacent to collapsed cfb
                    eft1 = tricubichermite.createEftNoCrossDerivatives()
                    remapEftNodeValueLabel(eft1, [ 6, 8 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS3, []) ])
                elif (e2 == (elementsCountUpAtria - 1)) and (e1 >= elementsCountRidgeVenous) and \
                        (e1 < (elementsCountAroundAtrialFreeWall - elementsCountRidgeVenous)):
                    # 6 node pole elements
                    nids.pop(7)
                    nids.pop(3)
                    s = e1 - elementsCountRidgeVenous
                    radiansAround0 = -0.5*math.pi + s*radiansPerElementAroundEnd
                    radiansAround1 = radiansAround0 + radiansPerElementAroundEnd
                    # scale factor identifiers follow convention of offsetting by 100 for each 'version'
                    eft1 = tricubichermite.createEftShellPoleTop(s*100, (s + 1)*100)
                    scalefactors = [
                        -1.0,
                        math.cos(radiansAround0), math.sin(radiansAround0), radiansPerElementAroundEnd,
                        math.cos(radiansAround1), math.sin(radiansAround1), radiansPerElementAroundEnd,
                        math.cos(radiansAround0), math.sin(radiansAround0), radiansPerElementAroundEnd,
                        math.cos(radiansAround1), math.sin(radiansAround1), radiansPerElementAroundEnd
                    ]
                elif (e2 == (elementsCountUpAtria - 1)) and (e1 < (elementsCountAroundAtrialFreeWall//2)):
                    # reverse d1 and d2 on ridge
                    eft1 = tricubichermite.createEftNoCrossDerivatives()
                    setEftScaleFactorIds(eft1, [1], [])
                    scaleEftNodeValueLabels(eft1, [ 3, 4, 7, 8 ], [ Node.VALUE_LABEL_D_DS1, Node.VALUE_LABEL_D_DS2 ], [ 1 ])

                if eft1 is not eft:
                    elementtemplateX.defineField(coordinates, -1, eft1)
                    elementtemplate1 = elementtemplateX

                element = mesh.createElement(elementIdentifier, elementtemplate1)
                result2 = element.setNodesByIdentifier(eft1, nids)
                if scalefactors:
                    result3 = element.setScaleFactors(eft1, scalefactors)
                elif eft1.getNumberOfLocalScaleFactors() == 1:
                    result3 = element.setScaleFactors(eft1, [ -1.0 ])
                else:
                    result3 = ' '
                #print('create element ra', element.isValid(), elementIdentifier, result2, result3, nids)
                elementIdentifier += 1

                for meshGroup in meshGroups:
                    meshGroup.addElement(element)

        # create first row of septum elements

        meshGroups = [ laMeshGroup, raMeshGroup, aSeptumMeshGroup ]
        for e1 in range(elementsCountFossaBase):
            n1l = elementsCountAroundAtrialFreeWall + e1 - elementsCountAroundAtria
            n1r = ran1FreeWallStart - e1
            if (elementsCountAroundAtrialSeptum == 2) and (e1 > 1):
                n1l -= 1
                n1r += 1
            nf1 = e1 - 1
            nf2 = e1
            nids = [ laNodeId[0][0][n1l], laNodeId[0][0][n1l + 1], fossaNodeId[0][nf1], fossaNodeId[0][nf2], \
                     raNodeId[0][0][n1r], raNodeId[0][0][n1r - 1], fossaNodeId[1][nf1], fossaNodeId[1][nf2] ]
            eft1 = tricubichermite.createEftNoCrossDerivatives()
            setEftScaleFactorIds(eft1, [1], [])
            if e1 == 0:
                nids[2] = laNodeId[0][1][n1l]
                nids[6] = raNodeId[0][1][n1r]
                scaleEftNodeValueLabels(eft1, [ 5, 6, 7 ], [ Node.VALUE_LABEL_D_DS1 ], [ 1 ])
                scaleEftNodeValueLabels(eft1, [ 6 ], [ Node.VALUE_LABEL_D_DS3 ], [ 1 ])
                remapEftNodeValueLabel(eft1, [ 1, 3 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS3, [] ) ])
                remapEftNodeValueLabel(eft1, [ 4, 8 ], Node.VALUE_LABEL_D_DS2, [ ( Node.VALUE_LABEL_D_DS1, [1] ), ( Node.VALUE_LABEL_D_DS2, [] ) ])
                remapEftNodeValueLabel(eft1, [ 4, 8 ], Node.VALUE_LABEL_D_DS1, [ ( Node.VALUE_LABEL_D_DS2, [] ) ])
                remapEftNodeValueLabel(eft1, [ 5, 7 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS3, [1] ) ])
                if elementsCountAroundAtrialSeptum == 2:
                    remapEftNodeValueLabel(eft1, [ 2 ], Node.VALUE_LABEL_D_DS2, [ ( Node.VALUE_LABEL_D_DS1, [1] ), ( Node.VALUE_LABEL_D_DS2, [] ) ])
                    remapEftNodeValueLabel(eft1, [ 6 ], Node.VALUE_LABEL_D_DS2, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS2, [] ) ])
            elif e1 == (elementsCountFossaBase - 1):
                nids[3] = laNodeId[0][1][n1l + 1]
                nids[7] = raNodeId[0][1][n1r - 1]
                scaleEftNodeValueLabels(eft1, [ 5, 6, 8 ], [ Node.VALUE_LABEL_D_DS1 ], [ 1 ])
                scaleEftNodeValueLabels(eft1, [ 5 ], [ Node.VALUE_LABEL_D_DS3 ], [ 1 ])
                remapEftNodeValueLabel(eft1, [ 2, 4 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [1] ), ( Node.VALUE_LABEL_D_DS3, [] ) ])
                remapEftNodeValueLabel(eft1, [ 3, 7 ], Node.VALUE_LABEL_D_DS2, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS2, [] ) ])
                remapEftNodeValueLabel(eft1, [ 3, 7 ], Node.VALUE_LABEL_D_DS1, [ ( Node.VALUE_LABEL_D_DS2, [1] ) ])
                remapEftNodeValueLabel(eft1, [ 6, 8 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [1] ), ( Node.VALUE_LABEL_D_DS3, [1] ) ])
                if elementsCountAroundAtrialSeptum == 2:
                    remapEftNodeValueLabel(eft1, [ 1 ], Node.VALUE_LABEL_D_DS2, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS2, [] ) ])
                    remapEftNodeValueLabel(eft1, [ 5 ], Node.VALUE_LABEL_D_DS2, [ ( Node.VALUE_LABEL_D_DS1, [1] ), ( Node.VALUE_LABEL_D_DS2, [] ) ])
            elif (elementsCountAroundAtrialSeptum == 2) and (e1 == 1):
                # 6-node wedge element
                nids.pop(5)
                nids.pop(1)
                scaleEftNodeValueLabels(eft1, [ 5, 6 ], [ Node.VALUE_LABEL_D_DS3 ], [ 1 ])
                remapEftNodeValueLabel(eft1, [ 1, 2, 5, 6 ], Node.VALUE_LABEL_D_DS1, [])
                remapEftNodeValueLabel(eft1, [ 1, 6 ], Node.VALUE_LABEL_D_DS2, [ ( Node.VALUE_LABEL_D_DS1, [1] ), ( Node.VALUE_LABEL_D_DS2, [] ) ])
                remapEftNodeValueLabel(eft1, [ 2, 5 ], Node.VALUE_LABEL_D_DS2, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS2, [] ) ])
                remapEftNodeValueLabel(eft1, [ 3, 7 ], Node.VALUE_LABEL_D_DS2, [ ( Node.VALUE_LABEL_D_DS1, [1] ), ( Node.VALUE_LABEL_D_DS2, [] ) ])
                remapEftNodeValueLabel(eft1, [ 4, 8 ], Node.VALUE_LABEL_D_DS2, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS2, [] ) ])
                ln_map = [ 1, 1, 2, 3, 4, 4, 5, 6 ]
                remapEftLocalNodes(eft1, 6, ln_map)
            else:
                scaleEftNodeValueLabels(eft1, [ 5, 6 ], [ Node.VALUE_LABEL_D_DS1 ], [ 1 ])
                scaleEftNodeValueLabels(eft1, [ 5, 6 ], [ Node.VALUE_LABEL_D_DS3 ], [ 1 ])
                if e1 == 1:
                    remapEftNodeValueLabel(eft1, [ 3, 7 ], Node.VALUE_LABEL_D_DS2, [ ( Node.VALUE_LABEL_D_DS1, [1] ), ( Node.VALUE_LABEL_D_DS2, [] ) ])
                if e1 == (elementsCountFossaBase - 2):
                    remapEftNodeValueLabel(eft1, [ 4, 8 ], Node.VALUE_LABEL_D_DS2, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS2, [] ) ])

            elementtemplateX.defineField(coordinates, -1, eft1)
            element = mesh.createElement(elementIdentifier, elementtemplateX)
            #print('e1',e1,'nids',nids)
            result2 = element.setNodesByIdentifier(eft1, nids)
            if eft1.getNumberOfLocalScaleFactors() == 1:
                result3 = element.setScaleFactors(eft1, [ -1.0 ])
            #print('create element septum base', element.isValid(), elementIdentifier, result2, result3, nids)
            elementIdentifier += 1

            for meshGroup in meshGroups:
                meshGroup.addElement(element)

        # septum arch over fossa ovalis

        meshGroups = [ laMeshGroup, raMeshGroup, aSeptumMeshGroup ]
        for e1 in range(2*(elementsCountUpAtria - 1)):
            eft1 = tricubichermite.createEftNoCrossDerivatives()
            setEftScaleFactorIds(eft1, [1], [])
            nids = None
            nf1 = e1 + elementsCountFossaBaseCentre
            nf2 = (nf1 + 1) % elementsCountAroundFossa
            if e1 < (elementsCountUpAtria - 1):
                n2 = e1 + 1
                n1l = 0
                n1r = -1
                nids = [ laNodeId[0][n2][n1l], laNodeId[0][n2 + 1][n1l], fossaNodeId[0][nf1], fossaNodeId[0][nf2], \
                         raNodeId[0][n2][n1r], raNodeId[0][n2 + 1][n1r], fossaNodeId[1][nf1], fossaNodeId[1][nf2] ]
                # set derivative 1 after 2 to swap:
                remapEftNodeValueLabel(eft1, [ 1, 2 ], Node.VALUE_LABEL_D_DS2, [ ( Node.VALUE_LABEL_D_DS1, [1] ) ])
                remapEftNodeValueLabel(eft1, [ 1, 2 ], Node.VALUE_LABEL_D_DS1, [ ( Node.VALUE_LABEL_D_DS2, [] ) ])
                remapEftNodeValueLabel(eft1, [ 1, 2 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [1] ), ( Node.VALUE_LABEL_D_DS3, [] ) ])
                remapEftNodeValueLabel(eft1, [ 5, 6 ], Node.VALUE_LABEL_D_DS1, [ ( Node.VALUE_LABEL_D2_DS1DS2, [] ) ])  # temporary to enable swap
                remapEftNodeValueLabel(eft1, [ 5, 6 ], Node.VALUE_LABEL_D_DS2, [ ( Node.VALUE_LABEL_D_DS1, [] ) ])
                remapEftNodeValueLabel(eft1, [ 5, 6 ], Node.VALUE_LABEL_D2_DS1DS2, [ ( Node.VALUE_LABEL_D_DS2, [] ) ])  # finish swap
                remapEftNodeValueLabel(eft1, [ 5, 6 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [1] ), ( Node.VALUE_LABEL_D_DS3, [1] ) ])
            else:
                n2 = 2*(elementsCountUpAtria - 1) - e1 + 1
                n1l = elementsCountAroundAtrialFreeWall
                n1r = elementsCountAroundAtrialSeptum - 1
                nids = [ laNodeId[0][n2][n1l], laNodeId[0][n2 - 1][n1l], fossaNodeId[0][nf1], fossaNodeId[0][nf2], \
                         raNodeId[0][n2][n1r], raNodeId[0][n2 - 1][n1r], fossaNodeId[1][nf1], fossaNodeId[1][nf2] ]
                if n2 == elementsCountUpAtria:
                    remapEftNodeValueLabel(eft1, [ 1 ], Node.VALUE_LABEL_D_DS2, [ ( Node.VALUE_LABEL_D_DS1, [1] ) ])
                    remapEftNodeValueLabel(eft1, [ 1 ], Node.VALUE_LABEL_D_DS1, [ ( Node.VALUE_LABEL_D_DS2, [] ) ])
                    remapEftNodeValueLabel(eft1, [ 1 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [1] ), ( Node.VALUE_LABEL_D_DS3, [] ) ])
                    remapEftNodeValueLabel(eft1, [ 2 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS3, [] ) ])
                    remapEftNodeValueLabel(eft1, [ 5 ], Node.VALUE_LABEL_D_DS1, [ ( Node.VALUE_LABEL_D2_DS1DS2, [] ) ])  # temporary to enable swap
                    remapEftNodeValueLabel(eft1, [ 5 ], Node.VALUE_LABEL_D_DS2, [ ( Node.VALUE_LABEL_D_DS1, [] ) ])
                    remapEftNodeValueLabel(eft1, [ 5 ], Node.VALUE_LABEL_D2_DS1DS2, [ ( Node.VALUE_LABEL_D_DS2, [] ) ])  # finish swap
                    remapEftNodeValueLabel(eft1, [ 5 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [1] ), ( Node.VALUE_LABEL_D_DS3, [1] ) ])
                    remapEftNodeValueLabel(eft1, [ 6 ], Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS3, [1] ) ])
                    lnl = [ 2 ]
                    lnr = [ 6 ]
                else:
                    lnl = [ 1, 2 ]
                    lnr = [ 5, 6 ]
                remapEftNodeValueLabel(eft1, lnl, Node.VALUE_LABEL_D_DS1, [ ( Node.VALUE_LABEL_D_DS2, [1] ) ])
                remapEftNodeValueLabel(eft1, lnl, Node.VALUE_LABEL_D_DS2, [ ( Node.VALUE_LABEL_D_DS1, [] ) ])
                remapEftNodeValueLabel(eft1, lnl, Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS3, [] ) ])
                remapEftNodeValueLabel(eft1, lnr, Node.VALUE_LABEL_D_DS1, [ ( Node.VALUE_LABEL_D_DS2, [1] ) ])
                remapEftNodeValueLabel(eft1, lnr, Node.VALUE_LABEL_D_DS2, [ ( Node.VALUE_LABEL_D_DS1, [1] ) ])
                remapEftNodeValueLabel(eft1, lnr, Node.VALUE_LABEL_D_DS3, [ ( Node.VALUE_LABEL_D_DS1, [] ), ( Node.VALUE_LABEL_D_DS3, [1] ) ])

            elementtemplateX.defineField(coordinates, -1, eft1)
            element = mesh.createElement(elementIdentifier, elementtemplateX)
            result2 = element.setNodesByIdentifier(eft1, nids)
            result3 = element.setScaleFactors(eft1, [ -1.0 ])
            #print('create element septum arch', element.isValid(), elementIdentifier, result2, result3, nids)
            elementIdentifier = elementIdentifier + 1

            for meshGroup in meshGroups:
                meshGroup.addElement(element)

        # fossa ovalis elements

        meshGroups = [ laMeshGroup, raMeshGroup, aSeptumMeshGroup, fossaMeshGroup ]
        radiansAround0 = fossaRadiansAround[-1] - 2.0*math.pi
        for e1 in range(elementsCountAroundFossa):
            va = e1
            vb = (e1 + 1)%elementsCountAroundFossa
            eft1 = tricubichermite.createEftShellPoleTop(va*100, vb*100)
            elementtemplateX.defineField(coordinates, -1, eft1)
            element = mesh.createElement(elementIdentifier, elementtemplateX)
            nids = [ fossaNodeId[0][va], fossaNodeId[0][vb], fossaCentreNodeId[0], fossaNodeId[1][va], fossaNodeId[1][vb], fossaCentreNodeId[1] ]
            result2 = element.setNodesByIdentifier(eft1, nids)
            radiansAround1 = fossaRadiansAround[va]
            radiansAround2 = fossaRadiansAround[vb]
            if radiansAround2 < radiansAround1:
                radiansAround2 += 2.0*math.pi
            radiansAround3 = fossaRadiansAround[vb + 1 - elementsCountAroundFossa]
            if radiansAround3 < radiansAround2:
                radiansAround3 += 2.0*math.pi
            dRadiansAround1 = 0.5*(radiansAround2 - radiansAround0)
            dRadiansAround2 = 0.5*(radiansAround3 - radiansAround1)
            scalefactors = [
                -1.0,
                -math.cos(radiansAround1), -math.sin(radiansAround1), dRadiansAround1,
                -math.cos(radiansAround2), -math.sin(radiansAround2), dRadiansAround2,
                -math.cos(radiansAround1), -math.sin(radiansAround1), dRadiansAround1,
                -math.cos(radiansAround2), -math.sin(radiansAround2), dRadiansAround2
            ]
            result3 = element.setScaleFactors(eft1, scalefactors)
            #print('create element fossa', element.isValid(), elementIdentifier, result2, result3, nids)
            elementIdentifier = elementIdentifier + 1

            for meshGroup in meshGroups:
                meshGroup.addElement(element)
            radiansAround0 = radiansAround1

        # create pulmonary vein inlets to left atrium

        # GRC fudgefactors, multiple of inner radius that inlet centre is away from septum
        rpvSeptumDistanceFactor = 2.0
        mx, md1 = getCubicHermiteCurvesPointAtArcDistance(rx, rd1, 0.5*aSeptumThickness + rpvSeptumDistanceFactor*rpvInnerRadius + rx[0][0])[0:2]
        laSeptumModX = aBaseInnerMajorMag*math.cos(aMajorAxisRadians)*math.cos(laSeptumRadians) \
                     + aBaseInnerMinorMag*math.sin(aMajorAxisRadians)*math.sin(laSeptumRadians)
        laOuterMajorx =  [ aBaseOuterMajorMag*math.cos(aMajorAxisRadians), -aBaseOuterMajorMag*math.sin(aMajorAxisRadians), 0.0 ]
        laOuterMinorx =  [ aBaseOuterMinorMag*math.sin(aMajorAxisRadians),  aBaseOuterMinorMag*math.cos(aMajorAxisRadians), 0.0 ]
        rpvdx = laSeptumModX + mx[0] + 0.5*aSeptumThickness
        rapvBaseRadians = getEllipseRadiansToX(laOuterMajorx[0], laOuterMinorx[0], rpvdx, laSeptumRadians + 0.5*math.pi)
        rppvBaseRadians = getEllipseRadiansToX(laOuterMajorx[0], laOuterMinorx[0], rpvdx, laSeptumRadians - 0.5*math.pi)

        ax = [ laCentre[c] + laOuterMajorx[c]*math.cos(rapvBaseRadians) + laOuterMinorx[c]*math.sin(rapvBaseRadians) for c in range(3) ]
        ad2 = [ 0.0, math.sin(aBaseFrontInclineRadians), math.cos(aBaseFrontInclineRadians) ]
        bx = [ laCentre[c] + laOuterMajorx[c]*math.cos(rppvBaseRadians) + laOuterMinorx[c]*math.sin(rppvBaseRadians) for c in range(3) ]
        bd2 = [ 0.0, math.sin(aBaseBackInclineRadians), -math.cos(aBaseBackInclineRadians) ]
        md2 = [ 0.5*(bx[0] - ax[0]), 0.5*(bx[1] - ax[1]), 0.0 ]

        if False:
            node = nodes.createNode(nodeIdentifier, nodetemplate)
            cache.setNode(node)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_VALUE, 1, mx)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS1, 1, md1)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS2, 1, md2)
            nodeIdentifier += 1

            node = nodes.createNode(nodeIdentifier, nodetemplate)
            cache.setNode(node)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_VALUE, 1, ax)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS2, 1, ad2)
            nodeIdentifier += 1

            node = nodes.createNode(nodeIdentifier, nodetemplate)
            cache.setNode(node)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_VALUE, 1, bx)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS2, 1, bd2)
            nodeIdentifier += 1

        px, pd1 = sampleCubicHermiteCurves([ ax, mx, bx ], [ ad2, md2, bd2 ], 2,
            lengthFractionEnd = rpvPositionUp/(2.0 - rpvPositionUp), arcLengthDerivatives = True)[0:2]
        rcpvx = px[1]
        rcpvd1 = pd1[1]

        if False:
            node = nodes.createNode(nodeIdentifier, nodetemplate)
            cache.setNode(node)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_VALUE, 1, rcpvx)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS1, 1, rcpvd1)
            nodeIdentifier += 1

        ex = sampleCubicHermiteCurves([ laOuterx[0][n1MidFreeWall], vx ],
            [ laOuterd2[0][n1MidFreeWall], vd2 ], elementsCountOut = 2,
            lengthFractionStart = lpvPositionUp/(1.0 - lpvPositionUp), arcLengthDerivatives = True)[0]
        lcpvx = ex[1]

        if False:
            node = nodes.createNode(nodeIdentifier, nodetemplate)
            cache.setNode(node)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_VALUE, 1, lcpvx)
            nodeIdentifier += 1

        lpvSpacingFactor = 2.0 if (lpvCount == 2) else 0.0
        rpvSpacingFactor = 2.0 if (rpvCount == 2) else 0.0
        pvDerivativeFactor = 1.0/elementsCountInlet  # GRC fudge factor
        rcpvWalld3 = vector.normalise([ (lcpvx[c] - rcpvx[c]) for c in range(3) ])
        rcpvWalld2 = vector.normalise(vector.crossproduct3(rcpvd1, rcpvWalld3))
        rcpvWalld1 = vector.crossproduct3(rcpvWalld2, rcpvWalld3)
        lcpvWalld1 = [ -d for d in rcpvWalld1 ]
        lcpvWalld2 = rcpvWalld2
        lcpvWalld3 = [ -d for d in rcpvWalld3 ]
        cosLpvAngleUpRadians = math.cos(lpvAngleUpRadians)
        sinLpvAngleUpRadians = math.sin(lpvAngleUpRadians)
        lcpvWalld3 = [ (lcpvWalld3[c]*cosLpvAngleUpRadians + lcpvWalld2[c]*sinLpvAngleUpRadians) for c in range(3) ]
        lcpvWalld2 = vector.crossproduct3(lcpvWalld3, lcpvWalld1)
        cosRpvAngleUpRadians = math.cos(rpvAngleUpRadians)
        sinRpvAngleUpRadians = math.sin(rpvAngleUpRadians)
        rcpvWalld3 = [ (rcpvWalld3[c]*cosRpvAngleUpRadians + rcpvWalld2[c]*sinRpvAngleUpRadians) for c in range(3) ]
        rcpvWalld2 = vector.crossproduct3(rcpvWalld3, rcpvWalld1)

        lipvCentred1 = vector.setMagnitude(lcpvWalld1, lpvInnerRadius)
        lipvCentred2 = vector.setMagnitude(lcpvWalld2, lpvInnerRadius)
        lipvCentred3 = vector.setMagnitude(lcpvWalld3, 2.0*lpvLengthFactor*lpvInnerRadius)
        lipvCentrex = [ (lcpvx[c] + lpvSpacingFactor*lipvCentred1[c] - lipvCentred3[c]) for c in range(3) ]
        lipvCentred3 = [ pvDerivativeFactor*d for d in lipvCentred3 ]

        lspvCentred1 = vector.setMagnitude(lcpvWalld1, lpvInnerRadius)
        lspvCentred2 = vector.setMagnitude(lcpvWalld2, lpvInnerRadius)
        lspvCentred3 = vector.setMagnitude(lcpvWalld3, 2.0*lpvLengthFactor*lpvInnerRadius)
        lspvCentrex = [ (lcpvx[c] - lpvSpacingFactor*lspvCentred1[c] - lspvCentred3[c]) for c in range(3) ]
        lspvCentred3 = [ pvDerivativeFactor*d for d in lspvCentred3 ]

        ripvCentred1 = vector.setMagnitude(rcpvWalld1, rpvInnerRadius)
        ripvCentred2 = vector.setMagnitude(rcpvWalld2, rpvInnerRadius)
        ripvCentred3 = vector.setMagnitude(rcpvWalld3, 2.0*rpvLengthFactor*rpvInnerRadius)
        ripvCentrex = [ (rcpvx[c] - rpvSpacingFactor*ripvCentred1[c] - ripvCentred3[c]) for c in range(3) ]
        ripvCentred3 = [ pvDerivativeFactor*d for d in ripvCentred3 ]

        rspvCentred1 = vector.setMagnitude(rcpvWalld1, rpvInnerRadius)
        rspvCentred2 = vector.setMagnitude(rcpvWalld2, rpvInnerRadius)
        rspvCentred3 = vector.setMagnitude(rcpvWalld3, 2.0*rpvLengthFactor*rpvInnerRadius)
        rspvCentrex = [ (rcpvx[c] + rpvSpacingFactor*rspvCentred1[c] - rspvCentred3[c]) for c in range(3) ]
        rspvCentred3 = [ pvDerivativeFactor*d for d in rspvCentred3 ]

        if False:
            node = nodes.createNode(nodeIdentifier, nodetemplate)
            cache.setNode(node)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_VALUE, 1, lipvCentrex)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS1, 1, lipvCentred1)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS2, 1, lipvCentred2)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS3, 1, lipvCentred3)
            nodeIdentifier += 1

            node = nodes.createNode(nodeIdentifier, nodetemplate)
            cache.setNode(node)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_VALUE, 1, lspvCentrex)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS1, 1, lspvCentred1)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS2, 1, lspvCentred2)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS3, 1, lspvCentred3)
            nodeIdentifier += 1

            node = nodes.createNode(nodeIdentifier, nodetemplate)
            cache.setNode(node)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_VALUE, 1, ripvCentrex)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS1, 1, ripvCentred1)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS2, 1, ripvCentred2)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS3, 1, ripvCentred3)
            nodeIdentifier += 1

            node = nodes.createNode(nodeIdentifier, nodetemplate)
            cache.setNode(node)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_VALUE, 1, rspvCentrex)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS1, 1, rspvCentred1)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS2, 1, rspvCentred2)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS3, 1, rspvCentred3)
            nodeIdentifier += 1

        # create left and right pulmonary veins
        pvCount = (lpvCount + rpvCount) if addInlets else 0

        for i in range(pvCount):
            if i < lpvCount:
                elementsCountAcrossInlet = elementsCountAcrossLPV
                elementsCountUpInlet = elementsCountUpLPV
                elementsCountAroundInlet = elementsCountAroundLPV
                inletInnerRadius = lpvInnerRadius
                inletWallThickness = lpvWallThickness
                if lpvCount == 1:
                    inletCentrex  = lipvCentrex
                    inletCentred1 = lipvCentred1
                    inletCentred2 = lipvCentred2
                    inletCentred3 = lipvCentred3
                    e1min = lipve1min
                    e2min = lipve2min
                    startRadians = 0.5*elementsCountUpInlet*math.pi/elementsCountAroundInlet
                    inletMeshGroups = [ lipvMeshGroup, lspvMeshGroup ]
                else:
                    if i == (lpvCount - 2):  # lipv
                        inletCentrex  = lipvCentrex
                        inletCentred1 = lipvCentred1
                        inletCentred2 = lipvCentred2
                        inletCentred3 = lipvCentred3
                        e1min = lipve1min
                        e2min = lipve2min
                        startRadians = 0.5*elementsCountUpInlet*math.pi/elementsCountAroundInlet
                        inletMeshGroups = [ lipvMeshGroup ]
                    else:  # lspv or single lpv
                        inletCentrex  = lspvCentrex
                        inletCentred1 = lspvCentred1
                        inletCentred2 = lspvCentred2
                        inletCentred3 = lspvCentred3
                        e1min = lspve1min
                        e2min = lspve2min
                        startRadians = 0.5*elementsCountUpInlet*math.pi/elementsCountAroundInlet
                        inletMeshGroups = [ lspvMeshGroup ]
            else:  # rpv
                elementsCountAcrossInlet = elementsCountAcrossRPV
                elementsCountUpInlet = elementsCountUpRPV
                elementsCountAroundInlet = elementsCountAroundRPV
                inletInnerRadius = rpvInnerRadius
                inletWallThickness = rpvWallThickness
                if rpvCount == 1:
                    inletCentrex  = ripvCentrex
                    inletCentred1 = ripvCentred1
                    inletCentred2 = ripvCentred2
                    inletCentred3 = ripvCentred3
                    e1min = ripve1min
                    e2min = ripve2min
                    startRadians = (2*elementsCountUpInlet + elementsCountAcrossInlet)*math.pi/elementsCountAroundInlet
                    inletMeshGroup = [ ripvMeshGroup, rspvMeshGroup ]
                else:
                    if i == (lpvCount + rpvCount - 2):  # ripv; unused if single rpv
                        inletCentrex  = ripvCentrex
                        inletCentred1 = ripvCentred1
                        inletCentred2 = ripvCentred2
                        inletCentred3 = ripvCentred3
                        e1min = ripve1min
                        e2min = ripve2min
                        startRadians = (2*elementsCountUpInlet + elementsCountAcrossInlet)*math.pi/elementsCountAroundInlet
                        inletMeshGroups = [ ripvMeshGroup ]
                    else:  # rspv or single rpv
                        inletCentrex  = rspvCentrex
                        inletCentred1 = rspvCentred1
                        inletCentred2 = rspvCentred2
                        inletCentred3 = rspvCentred3
                        e1min = rspve1min
                        e2min = rspve2min
                        startRadians = -0.75*elementsCountUpInlet*math.pi/elementsCountAroundInlet
                        inletMeshGroups = [ rspvMeshGroup ]

            inletStartInnerx, inletStartInnerd1 = createCirclePoints(inletCentrex, inletCentred1, inletCentred2, elementsCountAroundInlet, startRadians)
            inletStartOuterx, inletStartOuterd1 = createCirclePoints(inletCentrex, vector.setMagnitude(inletCentred1, inletInnerRadius + inletWallThickness), \
                vector.setMagnitude(inletCentred2, inletInnerRadius + inletWallThickness), elementsCountAroundInlet, startRadians)
            inletStartx  = [ inletStartInnerx , inletStartOuterx  ]
            inletStartd1 = [ inletStartInnerd1, inletStartOuterd1 ]
            inletStartd2 = [ [ inletCentred3 ]*elementsCountAroundInlet ]*2

            inletEndx = [ [], [] ]
            inletEndd1 = [ [], [] ]
            inletEndd2 = [ [], [] ]
            inletEndd3 = [ [], [] ]
            inletEndNodeId = [ [], [] ]
            inletEndDerivativesMap = [ [], [] ]
            n1min = e1min
            n1max = e1min + elementsCountAcrossInlet
            n2min = e2min
            n2max = e2min + elementsCountUpInlet
            for n3 in range(2):
                if n3 == 0:
                    lax  = laInnerx
                    lad1 = laInnerd1
                    lad2 = laInnerd2
                    lad3 = laInnerd3
                else:
                    lax  = laOuterx
                    lad1 = laOuterd1
                    lad2 = laOuterd2
                    lad3 = laOuterd3
                for n in range(elementsCountAroundInlet):
                    if n < elementsCountAcrossInlet:
                        # left
                        derivativesMap = [ ( 0, -1, 0 ), ( 1, -1, 0 ), None, ( -1, 0, 0 ) ] if (n == 0) else [ ( -1, 0, 0 ), ( 0, -1, 0 ), None ]
                        n1 = n1max - n
                        n2 = n2min
                    elif n < (elementsCountAcrossInlet + elementsCountUpInlet):
                        # up
                        derivativesMap = [ ( -1, 0, 0 ), ( -1, -1, 0 ), None, ( 0, 1, 0 ) ] if (n == elementsCountAcrossInlet) else [ ( 0, 1, 0 ), ( -1, 0, 0 ), None ]
                        n1 = n1min
                        n2 = n2min + (n - elementsCountAcrossInlet)
                    elif i < lpvCount:
                        # lpv apex and down
                        if n == (elementsCountAcrossInlet + elementsCountUpInlet):
                            if lpvCount == 1:
                                derivativesMap = [ ( 0, 1, 0 ), ( -1, 0, 0 ), None ]
                            else:  # if lpvCount == 2:
                                if i == 0:
                                    derivativesMap = [ ( -1, 0, 0 ), ( -1, -1, 0 ), None, ( 0, 1, 0 ) ]
                                else:
                                    derivativesMap = [ (  0, 1, 0 ), ( -1,  1, 0 ), None, ( 1, 0, 0 ) ]
                            n1 = elementsCountRidgeVenous
                        else:
                            derivativesMap = [ ( 0, -1, 0 ), ( 1, 0, 0 ), None ]
                            n1 = n1max
                        n2 = n2max - (n - (elementsCountAcrossInlet + elementsCountUpInlet))
                    else:
                        # rpv right and down
                        if n < (elementsCountAcrossInlet*2 + elementsCountUpInlet):
                            # rpv right
                            derivativesMap = [ ( 0, 1, 0 ), ( -1, 1, 0 ), None, ( 1, 0, 0 ) ] if (n == (elementsCountAcrossInlet + elementsCountUpInlet)) else [ None, None, None ]
                            n1 = n1min + (n - (elementsCountAcrossInlet + elementsCountUpInlet))
                            n2 = n2max
                        else:
                            # rpv down
                            derivativesMap = [ ( 1, 0, 0 ), ( 1, 1, 0 ), None, ( 0, -1, 0 ) ] if (n == (elementsCountAcrossInlet*2 + elementsCountUpInlet)) else [ ( 0, -1, 0 ), ( 1, 0, 0 ), None ]
                            n1 = n1max
                            n2 = n2max - (n - (elementsCountAcrossInlet*2 + elementsCountUpInlet))
                    if i == lpvCount:
                        # ripv, or single rpv straddling ridge
                        if (n3 == 1) and (n1 == n1max):
                            # fix ripv derivative 3 mapping adjacent to collapsed nodes maps to ds1 + ds3
                            derivativesMap[2] = ( 1, 0, 1 )
                        if n2 >= elementsCountUpAtria:
                            # reverse derivatives 1 and 2 on ridge
                            derivativesMap[0] = ( -1,  0,  0) if (derivativesMap[0] is None) else ( -derivativesMap[0][0], -derivativesMap[0][1], derivativesMap[0][2])
                            derivativesMap[1] = (  0, -1,  0) if (derivativesMap[1] is None) else ( -derivativesMap[1][0], -derivativesMap[1][1], derivativesMap[1][2])
                            derivativesMap[2] = None          if (derivativesMap[2] is None) else ( -derivativesMap[2][0], -derivativesMap[2][1], derivativesMap[2][2])
                            if len(derivativesMap) > 3:
                                derivativesMap[3] = ( -1,  0,  0) if (derivativesMap[3] is None) else ( -derivativesMap[3][0], -derivativesMap[3][1], derivativesMap[3][2])
                            # mirror to get coordinates from anterior
                            n1 = elementsCountAroundAtrialFreeWall - n1
                            n2 = elementsCountUpAtria*2 - n2
                    elif (i == (lpvCount + 1)) and (n3 == 1) and (n1 == n1min):
                        # fix rspv derivative 3 mapping adjacent to collapsed nodes maps to -ds1 + ds3
                        derivativesMap[2] = ( -1, 0, 1 )

                    # get derivatives 1 and 2 from node as some have been reduced on la beside inlets
                    cache.setNode(nodes.findNodeByIdentifier(laNodeId[n3][n2][n1]))
                    result, d1 = coordinates.getNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS1, 1, 3)
                    result, d2 = coordinates.getNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS2, 1, 3)
                    inletEndx [n3].append(lax [n2][n1])
                    inletEndd1[n3].append(d1)
                    inletEndd2[n3].append(d2)
                    inletEndd3[n3].append(lad3[n2][n1])
                    inletEndNodeId[n3].append(laNodeId[n3][n2][n1])
                    inletEndDerivativesMap[n3].append(derivativesMap)

            nodeIdentifier, elementIdentifier = tricubichermite.createAnnulusMesh3d(
                inletStartx, inletStartd1, inletStartd2, None, None, None,
                inletEndx, inletEndd1, inletEndd2, inletEndd3, inletEndNodeId, inletEndDerivativesMap,
                nodetemplate, nodetemplateLinearS3, nodeIdentifier, elementIdentifier,
                elementsCountRadial = elementsCountInlet, maxEndThickness = 1.5*aFreeWallThickness,
                meshGroups = [ laMeshGroup ] + inletMeshGroups)

        # create vena cavae inlets to right atrium

        # get vena cava inlet positions
        # GRC fudgefactors, multiple of inner radius that inlet centre is away from septum
        ivcSeptumDistanceFactor = 1.0
        svcSeptumDistanceFactor = 1.0
        vcDerivativeFactor = 1.0/elementsCountInlet  # GRC fudge factor
        raSeptumModX = -aBaseInnerMajorMag*math.cos(aMajorAxisRadians)*math.cos(-laSeptumRadians) \
                      + aBaseInnerMinorMag*math.sin(aMajorAxisRadians)*math.sin(-laSeptumRadians)
        raOuterMajorx =  [ -aBaseOuterMajorMag*math.cos(aMajorAxisRadians), -aBaseOuterMajorMag*math.sin(aMajorAxisRadians), 0.0 ]
        raOuterMinorx =  [  aBaseOuterMinorMag*math.sin(aMajorAxisRadians), -aBaseOuterMinorMag*math.cos(aMajorAxisRadians), 0.0 ]
        ivcdx = raSeptumModX + ivcSeptumDistanceFactor*ivcInnerRadius
        ivcBaseRadians = getEllipseRadiansToX(raOuterMajorx[0], raOuterMinorx[0], ivcdx, -laSeptumRadians + 0.5*math.pi)
        svcdx = raSeptumModX + svcSeptumDistanceFactor*svcInnerRadius
        svcBaseRadians = getEllipseRadiansToX(raOuterMajorx[0], raOuterMinorx[0], svcdx, -laSeptumRadians - 0.5*math.pi)

        raCentre = [ -laCentre[0], laCentre[1], laCentre[2] ]
        ax = [ raCentre[c] + raOuterMajorx[c]*math.cos(svcBaseRadians) + raOuterMinorx[c]*math.sin(svcBaseRadians) for c in range(3) ]
        ad2 = [ 0.0, math.sin(aBaseFrontInclineRadians), math.cos(aBaseFrontInclineRadians) ]
        bx = [ raCentre[c] + raOuterMajorx[c]*math.cos(ivcBaseRadians) + raOuterMinorx[c]*math.sin(ivcBaseRadians) for c in range(3) ]
        bd2 = [ 0.0, math.sin(aBaseBackInclineRadians), -math.cos(aBaseBackInclineRadians) ]
        # approximate middle point as half way between ax and bx at aOuterHeight
        mx = [ 0.5*(ax[0] + bx[0]), 0.5*(ax[1] + bx[1]), aOuterHeight ]
        md2 = [ 0.5*(bx[0] - ax[0]), 0.5*(bx[1] - ax[1]), 0.0 ]

        gap = 2.0 - svcPositionUp - ivcPositionUp
        px = sampleCubicHermiteCurves([ ax, mx, bx ], [ ad2, md2, bd2 ], elementsCountOut = 3, \
            lengthFractionStart = svcPositionUp/gap, lengthFractionEnd = ivcPositionUp/gap, arcLengthDerivatives = True)[0]
        svcWallx = px[1]
        ivcWallx = px[2]

        ivcWalld3 = vector.normalise([ (svcWallx[c] - ivcWallx[c]) for c in range(3) ])
        ivcWalld1 = vector.normalise([ ivcWalld3[1], -ivcWalld3[0], 0.0 ])
        ivcWalld2 = vector.crossproduct3(ivcWalld3, ivcWalld1)
        ivcDistance = 2.0*ivcLengthFactor*ivcInnerRadius

        cosIvcAngleUpRadians = math.cos(ivcAngleUpRadians)
        sinIvcAngleUpRadians = math.sin(ivcAngleUpRadians)

        ivcCentred1 = ivcWalld1
        ivcCentred2 = [ (ivcWalld2[c]*cosIvcAngleUpRadians - ivcWalld3[c]*sinIvcAngleUpRadians) for c in range(3) ]
        ivcCentred3 = [ (ivcWalld3[c]*cosIvcAngleUpRadians + ivcWalld2[c]*sinIvcAngleUpRadians) for c in range(3) ]

        if math.fabs(ivcAngleLeftRadians) < 1.0E-6:
            ivcCentrex = [ (ivcWallx[c] - ivcDistance*ivcCentred3[c]) for c in range(3) ]
        else:
            # rotate left is around a circular arc
            ivcTempd1 = ivcCentred1
            ivcTempd2 = ivcCentred2
            ivcTempd3 = ivcCentred3
            cosIvcAngleLeftRadians = math.cos(ivcAngleLeftRadians)
            sinIvcAngleLeftRadians = math.sin(ivcAngleLeftRadians)
            ivcCentred1 = [ (ivcTempd1[c]*cosIvcAngleLeftRadians - ivcTempd3[c]*sinIvcAngleLeftRadians) for c in range(3) ]
            ivcCentred2 = ivcTempd2
            ivcCentred3 = [ (ivcTempd3[c]*cosIvcAngleLeftRadians + ivcTempd1[c]*sinIvcAngleLeftRadians) for c in range(3) ]
            r = ivcDistance/ivcAngleLeftRadians
            offsetd1 = r*(1.0 - cosIvcAngleLeftRadians)
            offsetd3 = -r*sinIvcAngleLeftRadians
            ivcCentrex = [ (ivcWallx[c] + offsetd1*ivcCentred1[c] + offsetd3*ivcCentred3[c]) for c in range(3) ]
        ivcCentred1 = [ ivcInnerRadius*d for d in ivcCentred1 ]
        ivcCentred2 = [ ivcInnerRadius*d for d in ivcCentred2 ]
        ivcCentred3 = [ ivcDistance*vcDerivativeFactor*d for d in ivcCentred3 ]

        svcWalld3 = vector.normalise([ (ivcWallx[c] - svcWallx[c]) for c in range(3) ])
        svcWalld1 = vector.normalise([ svcWalld3[1], -svcWalld3[0], 0.0 ])
        svcWalld2 = vector.crossproduct3(svcWalld3, svcWalld1)
        svcDistance = 2.0*svcLengthFactor*svcInnerRadius
        cosSvcAngleUpRadians = math.cos(svcAngleUpRadians)
        sinSvcAngleUpRadians = math.sin(svcAngleUpRadians)
        svcCentred1 = vector.setMagnitude(svcWalld1, svcInnerRadius)
        svcCentred2 = [ svcInnerRadius*(svcWalld2[c]*cosSvcAngleUpRadians - svcWalld3[c]*sinSvcAngleUpRadians) for c in range(3) ]
        svcCentred3 = [ svcDistance   *(svcWalld3[c]*cosSvcAngleUpRadians + svcWalld2[c]*sinSvcAngleUpRadians) for c in range(3) ]
        svcCentrex = [ (svcWallx[c] - svcCentred3[c]) for c in range(3) ]
        svcCentred3 = [ vcDerivativeFactor*d for d in svcCentred3 ]

        if False:
            node = nodes.createNode(nodeIdentifier, nodetemplate)
            cache.setNode(node)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_VALUE, 1, ivcCentrex)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS1, 1, ivcCentred1)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS2, 1, ivcCentred2)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS3, 1, ivcCentred3)
            nodeIdentifier += 1

            node = nodes.createNode(nodeIdentifier, nodetemplate)
            cache.setNode(node)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_VALUE, 1, svcCentrex)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS1, 1, svcCentred1)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS2, 1, svcCentred2)
            coordinates.setNodeParameters(cache, -1, Node.VALUE_LABEL_D_DS3, 1, svcCentred3)
            nodeIdentifier += 1

        # create vena cavae

        elementsCountAcrossInlet = elementsCountAcrossVC
        for i in range(2 if addInlets else 0):
            if i == 0:  # ivc
                elementsCountUpInlet = elementsCountUpIVC
                elementsCountAroundInlet = elementsCountAroundIVC
                inletCentrex  = ivcCentrex
                inletCentred1 = ivcCentred1
                inletCentred2 = ivcCentred2
                inletCentred3 = ivcCentred3
                inletInnerRadius = ivcInnerRadius
                inletWallThickness = ivcWallThickness
                e1min = ivce1min
                e2min = ivce2min
            else:  # svc
                elementsCountUpInlet = elementsCountUpSVC
                elementsCountAroundInlet = elementsCountAroundSVC
                inletCentrex  = svcCentrex
                inletCentred1 = svcCentred1
                inletCentred2 = svcCentred2
                inletCentred3 = svcCentred3
                inletInnerRadius = svcInnerRadius
                inletWallThickness = svcWallThickness
                e1min = svce1min
                e2min = svce2min

            startRadians = elementsCountUpInlet*math.pi/elementsCountAroundInlet
            inletStartInnerx, inletStartInnerd1 = createCirclePoints(inletCentrex, inletCentred1, inletCentred2, elementsCountAroundInlet, startRadians)
            inletStartOuterx, inletStartOuterd1 = createCirclePoints(inletCentrex, vector.setMagnitude(inletCentred1, inletInnerRadius + inletWallThickness), \
                vector.setMagnitude(inletCentred2, inletInnerRadius + inletWallThickness), elementsCountAroundInlet, startRadians)
            inletStartx  = [ inletStartInnerx , inletStartOuterx  ]
            inletStartd1 = [ inletStartInnerd1, inletStartOuterd1 ]
            inletStartd2 = [ [ inletCentred3 ]*elementsCountAroundInlet ]*2

            inletEndx = [ [], [] ]
            inletEndd1 = [ [], [] ]
            inletEndd2 = [ [], [] ]
            inletEndd3 = [ [], [] ]
            inletEndNodeId = [ [], [] ]
            inletEndDerivativesMap = [ [], [] ]
            n1lmin = elementsCountAroundAtrialFreeWall - e1min - elementsCountAcrossInlet
            n1lmax = elementsCountAroundAtrialFreeWall - e1min
            n1rmin = ran1FreeWallStart + e1min
            n1rmax = n1rmin + elementsCountAcrossInlet
            for n3 in range(2):
                if n3 == 0:
                    lax  = laInnerx
                    lad1 = laInnerd1
                    lad2 = laInnerd2
                    lad3 = laInnerd3
                else:
                    lax  = laOuterx
                    lad1 = laOuterd1
                    lad2 = laOuterd2
                    lad3 = laOuterd3
                for n in range(elementsCountAroundInlet):
                    if n < elementsCountAcrossInlet:
                        # left
                        derivativesMap = [ ( 0, -1, 0 ), ( 1, -1, 0 ), None, ( -1, 0, 0 ) ] if (n == 0) else [ ( -1, 0, 0 ), ( 0, -1, 0 ), None ]
                        n1l = n1lmin + n
                        n1r = n1rmax - n
                        n2 = e2min
                    elif n < (elementsCountAcrossInlet + elementsCountUpInlet):
                        # up
                        derivativesMap = [ ( -1, 0, 0 ), ( -1, -1, 0 ), None, ( 0, 1, 0 ) ] if (n == elementsCountAcrossInlet) else [ ( 0, 1, 0 ), ( -1, 0, 0 ), None ]
                        n1l = n1lmax
                        n1r = n1rmin
                        n2 = e2min + n - elementsCountAcrossInlet
                    elif n < (elementsCountAcrossInlet*2 + elementsCountUpInlet):
                        # right
                        n1 = n - (elementsCountAcrossInlet + elementsCountUpInlet)
                        derivativesMap = [ ( 0, 1, 0 ), ( -1, 1, 0 ), None, ( 1, 0, 0 ) ] if (n1 == 0) else [ None, None, None ]
                        n1l = n1lmax - n1
                        n1r = n1rmin + n1
                        n2 = e2min + elementsCountUpInlet
                    else:
                        # down
                        n2 = elementsCountAroundInlet - n
                        derivativesMap = [ ( 1, 0, 0 ), ( 1, 1, 0 ), None, ( 0, -1, 0 ) ] if (n2 == elementsCountUpInlet) else [ ( 0, -1, 0 ), ( 1, 0, 0 ), None ]
                        n1l = n1lmin
                        n1r = n1rmax
                        n2 = e2min + elementsCountAroundInlet - n
                    if (i == 0) and (n3 == 1) and (n1r == n1rmin):
                        # fix ivc derivative 3 mapping adjacent to collapsed nodes maps to -ds1 + ds3
                        derivativesMap[2] = ( -1, 0, 1 )
                    elif (i == 1) and (n3 == 1) and (n1r == n1rmax):
                        # fix svc derivative 3 mapping adjacent to collapsed nodes maps to ds1 + ds3
                        derivativesMap[2] = ( 1, 0, 1 )
                    # mirror from left to right atrium
                    inletEndx [n3].append([ -lax [n2][n1l][0],  lax [n2][n1l][1],  lax [n2][n1l][2] ])
                    inletEndd1[n3].append([  lad1[n2][n1l][0], -lad1[n2][n1l][1], -lad1[n2][n1l][2] ])
                    inletEndd2[n3].append([ -lad2[n2][n1l][0],  lad2[n2][n1l][1],  lad2[n2][n1l][2] ])
                    inletEndd3[n3].append([ -lad3[n2][n1l][0],  lad3[n2][n1l][1],  lad3[n2][n1l][2] ])
                    #print('n',n,': n3',n3,'n2',n2,'n1r',n1r)
                    inletEndNodeId[n3].append(raNodeId[n3][n2][n1r])
                    inletEndDerivativesMap[n3].append(derivativesMap)

            nodeIdentifier, elementIdentifier = tricubichermite.createAnnulusMesh3d(
                inletStartx, inletStartd1, inletStartd2, None, None, None,
                inletEndx, inletEndd1, inletEndd2, inletEndd3, inletEndNodeId, inletEndDerivativesMap,
                nodetemplate, nodetemplateLinearS3, nodeIdentifier, elementIdentifier,
                elementsCountRadial = elementsCountInlet, maxEndThickness = 1.5*aFreeWallThickness,
                meshGroups = [ raMeshGroup, ivcInletMeshGroup if (i == 0) else svcInletMeshGroup])

        fm.endChange()
        return annotationGroups

    @classmethod
    def refineMesh(cls, meshrefinement, options):
        """
        Refine source mesh into separate region, with change of basis.
        :param meshrefinement: MeshRefinement, which knows source and target region.
        :param options: Dict containing options. See getDefaultOptions().
        """
        assert isinstance(meshrefinement, MeshRefinement)
        elementsCountAroundAtrialFreeWall = options['Number of elements around atrial free wall']
        elementsCountAroundAtrialSeptum = options['Number of elements around atrial septum']
        elementsCountAroundAtria = elementsCountAroundAtrialFreeWall + elementsCountAroundAtrialSeptum
        elementsCountUpAtria = options['Number of elements up atria']
        elementsCountInlet = options['Number of elements inlet']
        refineElementsCountSurface = options['Refine number of elements surface']
        refineElementsCountThroughWall = options['Refine number of elements through wall']
        element = meshrefinement._sourceElementiterator.next()
        sourceFm = meshrefinement._sourceFm
        annotationGroups = meshrefinement._sourceAnnotationGroups
        laGroup = findAnnotationGroupByName(annotationGroups, 'left atrium')
        laElementGroupField = laGroup.getFieldElementGroup(meshrefinement._sourceMesh)
        raGroup = findAnnotationGroupByName(annotationGroups, 'right atrium')
        raElementGroupField = raGroup.getFieldElementGroup(meshrefinement._sourceMesh)
        aSeptumGroup = findAnnotationGroupByName(annotationGroups, 'interatrial septum')
        aSeptumElementGroupField = aSeptumGroup.getFieldElementGroup(meshrefinement._sourceMesh)
        isSeptumEdgeWedge = sourceFm.createFieldXor(sourceFm.createFieldAnd(laElementGroupField, raElementGroupField), aSeptumElementGroupField)
        # last atria element is last element in svc inlet group:
        svcInletGroup = findAnnotationGroupByName(annotationGroups, 'superior vena cava inlet')
        svcInletMeshGroup = svcInletGroup.getMeshGroup(meshrefinement._sourceMesh)
        lastSvcInletElementIdentifier = -1
        elementIter = svcInletMeshGroup.createElementiterator()
        tmpElement = elementIter.next()
        while tmpElement.isValid():
            lastSvcInletElementIdentifier = tmpElement.getIdentifier()
            tmpElement = elementIter.next()

        cache = sourceFm.createFieldcache()

        refineElements2 = refineElementsCountSurface
        refineElements3 = refineElementsCountThroughWall
        while element.isValid():
            elementIdentifier = element.getIdentifier()
            cache.setElement(element)
            result, isWedge = isSeptumEdgeWedge.evaluateReal(cache, 1)
            if isWedge:
                refineElements1 = refineElementsCountThroughWall
            else:
                refineElements1 = refineElementsCountSurface
            meshrefinement.refineElementCubeStandard3d(element, refineElements1, refineElements2, refineElements3)
            if elementIdentifier == lastSvcInletElementIdentifier:
                return  # finish on last so can continue elsewhere
            element = meshrefinement._sourceElementiterator.next()

    @classmethod
    def generateMesh(cls, region, options):
        """
        Generate base or refined mesh.
        :param region: Zinc region to create mesh in. Must be empty.
        :param options: Dict containing options. See getDefaultOptions().
        :return: list of AnnotationGroup for mesh.
        """
        if not options['Refine']:
            return cls.generateBaseMesh(region, options)
        baseRegion = region.createRegion()
        baseAnnotationGroups = cls.generateBaseMesh(baseRegion, options)
        meshrefinement = MeshRefinement(baseRegion, region, baseAnnotationGroups)
        cls.refineMesh(meshrefinement, options)
        return meshrefinement.getAnnotationGroups()


def getLeftAtriumBasePoints(elementsCountAroundAtrialFreeWall, elementsCountAroundAtrialSeptum,
        aBaseInnerMajorMag, aBaseInnerMinorMag, aMajorAxisRadians,
        aBaseWallThickness, aBaseSlopeHeight, aBaseSlopeLength, aSeptumThickness,
        aortaOuterPlusRadius, aBaseFrontInclineRadians, aBaseSideInclineRadians, aBaseBackInclineRadians):
    """
    Get points around left atrium based on an ellipse. Points start from central fibrous body
    and wind anticlockwise around LA. Both the cfb and crux are collapsed at the septum.
    :return: laCentre, laSeptumRadians, laBaseInnerx, laBaseInnerd1, laBaseInnerd2, laBaseOuterx, laBaseOuterd1, laBaseOuterd2.
    """

    elementsCountAroundAtrium = elementsCountAroundAtrialFreeWall + elementsCountAroundAtrialSeptum
    lvOutletFrontInclineRadians = aBaseFrontInclineRadians  # for now

    aBaseOuterMajorMag = aBaseInnerMajorMag + aBaseSlopeLength
    aBaseOuterMinorMag = aBaseInnerMinorMag + aBaseSlopeLength

    # following are angles in radians around LA ellipse from major axis
    axInner = aBaseInnerMajorMag*math.cos(aMajorAxisRadians)
    bxInner = aBaseInnerMinorMag*math.sin(aMajorAxisRadians)
    laSeptumRadians = math.atan2(bxInner, axInner)
    laCentreX = -0.5*aSeptumThickness - axInner*math.cos(laSeptumRadians) - bxInner*math.sin(laSeptumRadians)
    #laCfbLeftRadians = updateEllipseAngleByArcLength(aBaseInnerMajorMag, aBaseInnerMinorMag, laSeptumRadians, \
    #    (aSeptumBaseLength/elementsCountAroundAtrialSeptum)*(0.5*elementsCountAroundAtrialSeptum + 1.0))
    axOuter = aBaseOuterMajorMag*math.cos(aMajorAxisRadians)
    bxOuter = aBaseOuterMinorMag*math.sin(aMajorAxisRadians)

    # get points on central fibrous body centre and cfbLeft (60 degrees clockwise around aorta)
    # rotates about centre of aorta by aBaseFrontInclineRadians
    cosFrontInclineRadians = math.cos(aBaseFrontInclineRadians)
    sinFrontInclineRadians = math.sin(aBaseFrontInclineRadians)
    pi_3 = math.pi/3.0
    cosPi_3 = math.cos(pi_3)
    sinPi_3 = math.sin(pi_3)
    cfbSideOffset = aortaOuterPlusRadius*sinPi_3
    rLeft = aortaOuterPlusRadius*cosPi_3
    cfbLeftX = -cfbSideOffset
    cfbLeftY = -rLeft*cosFrontInclineRadians
    cfbLeftZ = rLeft*sinFrontInclineRadians
    cfbX = 0.0
    cfbY = -aortaOuterPlusRadius*cosFrontInclineRadians
    cfbZ = aortaOuterPlusRadius*sinFrontInclineRadians
    lvOutletDerivativeAround = aortaOuterPlusRadius*pi_3
    laCfbLeftRadians = getEllipseRadiansToX(axOuter, bxOuter, cfbLeftX - laCentreX, math.pi*0.5)
    aBaseOuterMinorMagPlus = aBaseOuterMinorMag + 0.5*aBaseSlopeLength  # GRC fudge factor
    laCentreY = cfbLeftY - math.cos(laCfbLeftRadians)*aBaseOuterMajorMag*math.sin(-aMajorAxisRadians) \
                         - math.sin(laCfbLeftRadians)*aBaseOuterMinorMagPlus*math.cos(-aMajorAxisRadians)
    laCentreZ = 0.0

    # compute radians around based on base outer major and minor axis sizes
    atrialPerimeterLength = getApproximateEllipsePerimeter(aBaseOuterMajorMag, aBaseOuterMinorMag)
    atrialSeptumElementLength = getEllipseArcLength(aBaseOuterMajorMag, aBaseOuterMinorMag, laSeptumRadians, laCfbLeftRadians) \
        /(0.5*elementsCountAroundAtrialSeptum + 1.0)
    atrialFreeWallElementLength = (atrialPerimeterLength - atrialSeptumElementLength*(elementsCountAroundAtrialSeptum + 2)) \
        / (elementsCountAroundAtrialFreeWall - 2)
    atrialTransitionElementLength = 0.5*(atrialSeptumElementLength + atrialFreeWallElementLength)
    #atrialPerimeterLengthTmp = atrialSeptumElementLength*(elementsCountAroundAtrialSeptum + 1) + 2.0*atrialTransitionElementLength \
    #    + (elementsCountAroundAtrialFreeWall - 3)*atrialFreeWallElementLength
    #print('lengths:',(elementsCountAroundAtrialSeptum + 1),'*',atrialSeptumElementLength, '+ 2 *', \
    #    atrialTransitionElementLength,'+',(elementsCountAroundAtrialFreeWall - 3),'*',atrialFreeWallElementLength,
    #    '=', atrialPerimeterLengthTmp, ' VS ', atrialPerimeterLength)
    laRadians = []
    radiansAround = updateEllipseAngleByArcLength(aBaseOuterMajorMag, aBaseOuterMinorMag, laSeptumRadians, atrialSeptumElementLength*elementsCountAroundAtrialSeptum/2.0)
    for n1 in range(elementsCountAroundAtrium):
        laRadians.append(radiansAround)
        if (n1 == 0) or (n1 >= elementsCountAroundAtrialFreeWall):
            elementLength = atrialSeptumElementLength
        elif (n1 == 1) or (n1 == (elementsCountAroundAtrialFreeWall - 1)):
            elementLength = atrialTransitionElementLength
        else:
            elementLength = atrialFreeWallElementLength
        radiansAround = updateEllipseAngleByArcLength(aBaseOuterMajorMag, aBaseOuterMinorMag, radiansAround, elementLength)

    laBaseInnerx = []
    laBaseInnerd1 = []
    laBaseInnerd2 = []
    laBaseOuterx = []
    laBaseOuterd1 = []
    laBaseOuterd2 = []

    baseDerivative2Scale = aortaOuterPlusRadius
    sinMajorAxisRadians = math.sin(-aMajorAxisRadians)
    cosMajorAxisRadians = math.cos(-aMajorAxisRadians)

    # get base points on inside and outside of atria
    for n3 in range(2):
        if n3 == 0:
            aMajorMag = aBaseInnerMajorMag
            aMinorMag = aBaseInnerMinorMag
            z = -aBaseSlopeHeight
        else:
            aMajorMag = aBaseOuterMajorMag
            aMinorMag = aBaseOuterMinorMag
            z = 0.0

        aMajorX =  aMajorMag*cosMajorAxisRadians
        aMajorY =  aMajorMag*sinMajorAxisRadians
        aMinorX = -aMinorMag*sinMajorAxisRadians
        aMinorY =  aMinorMag*cosMajorAxisRadians

        twoPi = 2.0*math.pi
        finalArcLength = prevArcLength = getEllipseArcLength(aMajorMag, aMinorMag, laRadians[-1] - twoPi, laRadians[0])
        n1Limit = elementsCountAroundAtrium if (n3 == 0) else (elementsCountAroundAtrialFreeWall + 1)
        for n1 in range(n1Limit):
            radiansAround = laRadians[n1]
            cosRadiansAround = math.cos(radiansAround)
            sinRadiansAround = math.sin(radiansAround)

            # get derivative around
            if n1 == (elementsCountAroundAtrium - 1):
                nextArcLength = finalArcLength
            else:
                nextArcLength = getEllipseArcLength(aMajorMag, aMinorMag, laRadians[n1], laRadians[n1 + 1])
            if (n1 <= 1) or (n1 > elementsCountAroundAtrialFreeWall):
                derivativeAround = min(prevArcLength, nextArcLength)
            else:
                derivativeAround = max(prevArcLength, nextArcLength)
            prevArcLength = nextArcLength

            if (n3 == 1) and (n1 == 0):
                x = [ cfbX, cfbY, cfbZ ]
                d1 = [ -lvOutletDerivativeAround, 0.0, 0.0 ]
                d2 = [ 0.0, baseDerivative2Scale*sinFrontInclineRadians, baseDerivative2Scale*cosFrontInclineRadians ]
            elif (n3 == 1) and (n1 == 1):
                x = [ cfbLeftX, cfbLeftY, cfbLeftZ ]
                d1 = [ -lvOutletDerivativeAround*cosPi_3, lvOutletDerivativeAround*sinPi_3*cosFrontInclineRadians, -lvOutletDerivativeAround*sinPi_3*sinFrontInclineRadians ]
                d2 = [ 0.0, baseDerivative2Scale*sinFrontInclineRadians, baseDerivative2Scale*cosFrontInclineRadians ]
            else:
                x = [
                    laCentreX + cosRadiansAround*aMajorX + sinRadiansAround*aMinorX,
                    laCentreY + cosRadiansAround*aMajorY + sinRadiansAround*aMinorY,
                    z ]
                d1x = -sinRadiansAround*aMajorX + cosRadiansAround*aMinorX
                d1y = -sinRadiansAround*aMajorY + cosRadiansAround*aMinorY
                scale1 = derivativeAround/math.sqrt(d1x*d1x + d1y*d1y)
                d1 = [ d1x*scale1, d1y*scale1, 0.0 ]

                if (n3 == 0) or (n1 > elementsCountAroundAtrialFreeWall):
                    d2 = [ 0.0, 0.0, baseDerivative2Scale ]  # calculated later
                elif (n1 == elementsCountAroundAtrialFreeWall):
                    # get collapsed crux (outer back base septum) position and derivative:
                    xi = 0.9  # GRC fudge factor
                    nx  = [ laBaseOuterx [-1], [ 0.0, (1.0 - xi)*laBaseOuterx[0][1] + xi*laBaseOuterx[-1][1], 0.0 ] ]
                    nd1 = smoothCubicHermiteDerivativesLine(nx, [ laBaseOuterd1[-1], [ vector.magnitude(laBaseOuterd1[-1]), 0.0, 0.0 ] ],
                        fixStartDerivative = True, fixEndDirection = True )
                    x = nx[1]
                    # GRC fudge factor: derivative must be lower to fit inlets:
                    d1 = [ 0.35*d for d in nd1[1] ]
                    # derivative 2 slopes directly back = no x component
                    d2 = [ 0.0, -baseDerivative2Scale*math.sin(aBaseBackInclineRadians), baseDerivative2Scale*math.cos(aBaseBackInclineRadians) ]
                else:
                    baseInclineRadians = 0.0
                    sideRadians = laSeptumRadians + math.pi
                    backRadians = sideRadians + math.pi*0.5
                    if radiansAround < sideRadians:
                        xi = (radiansAround - laCfbLeftRadians)/sideRadians
                        baseInclineRadians = (1.0 - xi)*aBaseFrontInclineRadians + xi*aBaseSideInclineRadians
                    elif radiansAround < backRadians:
                        xi = (radiansAround - sideRadians)/(math.pi*0.5)
                        baseInclineRadians = (1.0 - xi)*aBaseSideInclineRadians + xi*aBaseBackInclineRadians
                    else:
                        baseInclineRadians = aBaseBackInclineRadians
                    scale2 = baseDerivative2Scale/vector.magnitude(d1)
                    side = [ d1[1]*scale2, -d1[0]*scale2, 0.0 ]
                    up = [ 0.0, 0.0, baseDerivative2Scale ]
                    d2 = [ (up[c]*math.cos(baseInclineRadians) + side[c]*math.sin(baseInclineRadians)) for c in range(3) ]

            if n3 == 0:
                laBaseInnerx.append(x)
                laBaseInnerd1.append(d1)
                laBaseInnerd2.append(d2)
            else:
                laBaseOuterx.append(x)
                laBaseOuterd1.append(d1)
                laBaseOuterd2.append(d2)

    for n1 in range(elementsCountAroundAtrialFreeWall + 1, elementsCountAroundAtrium):
        laBaseOuterx.append(None)
        laBaseOuterd1.append(None)
        laBaseOuterd2.append(None)

    return [ laCentreX, laCentreY, laCentreZ ], laSeptumRadians, laBaseInnerx, laBaseInnerd1, laBaseInnerd2, laBaseOuterx, laBaseOuterd1, laBaseOuterd2
