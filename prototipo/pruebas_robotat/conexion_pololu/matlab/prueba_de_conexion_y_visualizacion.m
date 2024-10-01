markers = [22];

robotat = robotat_connect();

pose = robotat_get_pose(robotat, markers,'eulzyx')

robotat_trvisualize(robotat,markers)