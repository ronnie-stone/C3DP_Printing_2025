import math
from datetime import datetime


class Conversion:

	def __init__(self, input_file, updated_file):
		self.input_file = input_file
		self.updated_file = updated_file

	def convert(self):

		filename = self.updated_file
		with open(self.input_file, "r", encoding="utf8") as myfile:
			with open(filename, "w", encoding='utf8') as replaced:

				for line in myfile.readlines():
					if 'Layer' in line:
						newline = line

					elif 'Interfacing' in line or "Non-interfacing" in line:
						newline = line

					else:
						data = line.split()
						x = float(data[0])
						y = float(data[1])
                        
						x_new = x
						y_new = y
                        
						newline = str(x_new) + ' ' + str(y_new) + ' ' + data[2] + ' '+data[3] + '\n'

					replaced.write(newline)

class ManualGcode:

	def __init__(self, tamu_file, initial_gcode, final_gcode_robot, diameter, layerHeight, linewidth):
		self.tamu_file = tamu_file
		self.initial_gcode = initial_gcode
		self.final_gcode_robot = final_gcode_robot
		self.diameter = diameter
		self.layerHeight = layerHeight
		self.linewidth = linewidth

	def extrusionCalculator(self, locations):
		diameter = self.diameter
		layerHeight = self.layerHeight
		linewidth = self.linewidth

		# locations used for calculation of the volume of extrusion
		x1 = locations[0][0]
		x2 = locations[1][0]
		y1 = locations[0][1]
		y2 = locations[1][1]
		length = math.hypot(x2-x1, y2-y1)

		#calcualate the area and then the volume of the cylinder
		areaRoad = (linewidth - layerHeight)*layerHeight+math.pi*((layerHeight/2)**2)
		exrudedAmount = areaRoad*length*4/(math.pi*diameter**2)

		return exrudedAmount

	def generateGcodeR1(self, layerHeight, AMBOTS=1):

		filename = 'AMBOT' + str(AMBOTS) + '_' + \
			str(datetime.now().strftime('%Y_%m_%d_%H_%M')) + '.gcode'
		z = 0
		# goToStart = "G0 X300 Y20 Z50 \n"
		# startup routine for the printers
		initial_gcode = self.initial_gcode
		with open(self.tamu_file, "r") as myfile:
			with open(filename, "w") as replaced:
				# set up initial parameters
				i = 0
				x_prev = 0
				y_prev = 0
				t_prev = 0
				lineprev = ""
				replaced.write(initial_gcode)

				for line in myfile.readlines():
					if 'Layer' in line:
						z += layerHeight
						lineprev = line
						layer_number = int(line.split("Layer")[1].strip())
						if layer_number != 1:
							newline = ";LAYER:" + str(layer_number-1) + "\n" + \
							"M25\n"
							replaced.write(newline)
					elif 'Interfacing' in line:
						if 'Layer' in lineprev:
							newline = "M117 Interfacing\n" + \
                            "M25\n" + \
                            "M104 S240\n"
							replaced.write(newline)
						else:
							newline = "M117 Interfacing\n"
							replaced.write(newline)
					elif "Non-interfacing" in line:
						if 'Layer' in lineprev:
							newline = "M117 Non-Interfacing\n" + \
                            "M25\n" + \
                            "M104 S240\n"
							replaced.write(newline)
						else:
							newline = "M117 Non-Interfacing\n"
							replaced.write(newline)

					else:
						# splits the line and assings x, y and t values
						data = line.split()

						# Printer 1:
						# x = float(data[0]) - 14
						# y = float(data[1]) + 7

						# Printer 2:
						x = float(data[0])
						y = float(data[1])
						# x_temp = float(data[0])
						# y_temp = float(data[1]) + 10 
						# angle_degrees = 1
						# angle_radians = math.radians(angle_degrees)
						# x = x_temp*(math.cos(angle_radians)) -  y_temp*(math.sin(angle_radians))
						# y = x_temp*(math.sin(angle_radians)) +  y_temp*(math.cos(angle_radians))
						# x = x + 5
						# y = y - 1.5

						# Printer 3:
						# x = float(data[0])
						# y = float(data[1])

		
						#Z = float(data[2])
						t = int(float(data[3]))

						if i == 0:
							newline = "G1 X" + str(x) + ' Y' + str(y) + '\n'
						else:
							points = [(x_prev, y_prev), (x, y)]
							if t_prev == 1:
								eValue = self.extrusionCalculator(points)
								newline = "G1 X" + str(x) + ' Y' + str(y) + ' Z' + str(z) + ' E' + str(eValue) + '\n'
							elif t_prev == 2:                    
								newline = "G92 E0\n" + \
                                    "G1 E-3.0000 F3000\n" + \
                                    "G0 Z" + str(z+5) + \
                                    "G0 X" + str(x) + ' Y' + str(y) + ' Z' + str(z+5) + '\n' + \
                                    "G0 Z" + str(z) + \
                                    "G1 E3.0000 F3000\n" + \
                                    "G92 E0\n"
							else:
								newline = "G0 X" + str(x) + ' Y' + str(y) + ' Z' + str(z) + '\n'
                                                
						replaced.write(newline)
						x_prev = float(x)
						y_prev = float(y)
						t_prev = t
						i = i + 1
						lineprev = line
				replaced.write(final_gcode)


if __name__ == '__main__':
	initial_gcode = ''';FLAVOR:RepRap
	;TIME:3347
	;Filament used: 6.02278m
	;Layer height: 0.4
	;MINX:230.638
	;MINY:75.325
	;MINZ:0.45
	;MAXX:239.988
	;MAXY:224.675
	;MAXZ:22.65
	;Generated with Cura_SteamEngine 5.2.2
	T0
	M104 S240
	M109 S240
	M82 ;absolute extrusion mode
	M104 S240
	;G28 Z ; Z
	G29 S1;
	M105
		M109 S240
		M82 ;absolute extrusion mode
		G1 Z15.0 F6000 ;Move the platform down 15mm
		;Prime the extruder
		G92 E0
		G1 F200 E3
		G92 E0
		M83 ;relative extrusion mode
		G1 F1200 E-5.6
		;LAYER_COUNT:80
		;LAYER:0
		M400
		M107
		M204 S5000
		G1 F600 Z5.0
		G0 F900 X215.005 Y128.49 Z5.0
		M204 S100
		;TYPE:WALL-OUTER
		G1 F600 Z5.0
		G1 F1200 E5.61568
	M83 ;relative extrusion mode
	G1 F3000 E-4
	;LAYER_COUNT:50
	;LAYER:0
	M107
	M204 T500
	M566 X1800 Y1800
	G1 F1800 Z5.0
	G0 X231.288 Y75.975 Z5.0
	M204 P100
	M566 X600 Y600
	;TYPE:WALL-INNER\n'''

	final_gcode = ''';TIME_ELAPSED:3347.927760
	G1 F3000 E-4
	M204 P4000
	M204 T4000
	M566 X1200 Y1200
	M82 ;absolute extrusion mode
	G1 F1200 E-5.6
		M204 S4000
		M82 ;absolute extrusion mode
		M104 S0
		M140 S0
		;Retract the filament
		G92 E1
		G1 E-1 F300
		G1 X290 Y10
		M84
		M82 ;absolute extrusion mode
		M104 S0
	M83 ;relative extrusion mode
	M104 S0
	;End of Gcode\n'''

	# For now, we will assume that the coordinate transformation of the TAMU files is correct.

	tamu_file = 'PrintingFiles/Einstein/R3_Einstein_300.txt'

	# convertfile = Conversion(tamu_file, updated_file)
	# convertfile.convert()

	# Parameters associated with the calculation of volume of extrusion

	diameter = 1.75
	layerHeight = 0.45 # change the height based on the file provided 
	linewidth = 0.42 #adjust to change extrusion rate (Was 0.42)

	createGcode = ManualGcode(tamu_file, initial_gcode, final_gcode, diameter, layerHeight, linewidth)
	createGcode.generateGcodeR1(layerHeight, AMBOTS="3")
