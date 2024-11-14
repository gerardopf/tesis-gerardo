markers = [22,21,20,2,3,4,5,11];

robotat = robotat_connect();

pose = robotat_get_pose(robotat, markers,'eulzyx')

robotat_trvisualize(robotat,markers)