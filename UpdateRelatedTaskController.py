#Input 
#	"task_id": t_id=7 

import sys
t_id=sys.argv[1]

import datetime

import kanboard
kb = kanboard.Client('http://192.168.100.221/kanboard/jsonrpc.php', 'jsonrpc', '392dc75baf66ae2205e9d0655a3e150c5766d011031658c7a1f3d152f5ef')

TaskProperties=kb.getTask(task_id=t_id)
AllInternalTaskLinks=kb.getAllTaskLinks(task_id=t_id)
AllTaskComments=kb.getAllComments(task_id=t_id)
AllTaskFiles=kb.getAllTaskFiles(task_id=t_id)
UpdateSwitch=0

for i in range(0,len(AllInternalTaskLinks)):
	InternalTaskLinkById=kb.getTaskLinkById(task_link_id=AllInternalTaskLinks[i]['id'])
	if InternalTaskLinkById['link_id']=='12' and InternalTaskLinkById['label']=='updatet':
		UpdateSwitch=1
		OppositeTask=kb.getTask(task_id=InternalTaskLinkById['opposite_task_id'])
		#Comment
		tmp_Comments=[]
		for j in range(0,len(AllTaskComments)):
			tmp_Comments.append("* "+datetime.datetime.fromtimestamp(int(AllTaskComments[j]["date_creation"])).isoformat()+" ("+datetime.datetime.fromtimestamp(int(AllTaskComments[j]["date_modification"])).isoformat()+"):\n'"+AllTaskComments[j]["comment"]+"'\n\n")
		tmp_CommentsMin=min(len(tmp_Comments), 2)
		tmp_CommentId=kb.createComment(task_id=InternalTaskLinkById['opposite_task_id'], user_id=0, content=''.join(tmp_Comments[::-1][:tmp_CommentsMin]))
		#Attachment
		tmp_AllTaskFiles=kb.removeAllTaskFiles(task_id=InternalTaskLinkById['opposite_task_id'])
		for j in range(0,len(AllTaskFiles)):
			DownloadTaskFile=kb.downloadTaskFile(file_id=AllTaskFiles[j]['id'])
			tmp_CreatedTaskFile=kb.createTaskFile(project_id=OppositeTask['project_id'], task_id=InternalTaskLinkById['opposite_task_id'], filename=AllTaskFiles[j]['name'], blob=DownloadTaskFile)
		#CopyInternalLinks
#		for j in range(0,len(AllInternalTaskLinks)):
#			if j!=i:
#				tmp_InternalTaskLinkById=kb.getTaskLinkById(task_link_id=AllInternalTaskLinks[j]['id'])
#				if tmp_InternalTaskLinkById is not None and tmp_InternalTaskLinkById['link_id']!='12':
##					kb.createTaskLink(task_id=UpdatedTaskID, opposite_task_id=tmp_InternalTaskLinkById['opposite_task_id'], link_id=tmp_InternalTaskLinkById['link_id'])
        	#Category
		if TaskProperties['category_id']!=OppositeTask['category_id']:
			tmp_TaskProperties=kb.updateTask(id=InternalTaskLinkById['opposite_task_id'], category_id=TaskProperties['category_id'])
		#Tag
		TaskTags=kb.getTaskTags(task_id=t_id)
#		dictlist=dict.items()
#		for key, value in dict.iteritems():
#			temp=[key, value]
#			dictlist.append(temp)
		OppositeTaskTags=kb.setTaskTags(project_id=OppositeTask['project_id'], task_id=InternalTaskLinkById['opposite_task_id'], tags=TaskTags)
#		tmp_AllTaskFiles=kb.getAllTaskFiles(task_id=t_id)
#		for j in range(0,len(tmp_AllTaskFiles)):
#			tmp_DownloadTaskFile=kb.downloadTaskFile(file_id=tmp_AllTaskFiles[j]['id'])
#			tmp_CreatedTaskFile=kb.createTaskFile(project_id=OppositeTaskToUpdate['project_id'], task_id=UpdatedTaskID, filename=tmp_AllTaskFiles[j]['name'], blob=tmp_DownloadTaskFile)
		#RemoveOldTask
#		tmp_removeTask=kb.removeTask(task_id=InternalTaskLinkById['opposite_task_id'])
if UpdateSwitch==0:
	print('Keine Karte zum Updaten (interne Verbindung: UPDATET) gefunden.')
elif UpdateSwitch==1:
##	tmp_AllTaskFiles=kb.getAllTaskFiles(task_id=t_id)#InternalTaskLinkById['opposite_task_id'])
	print(TaskTags)#'Alle Karten, die mit UPDATET intern verbunden sind, wurden geupdatet.')
