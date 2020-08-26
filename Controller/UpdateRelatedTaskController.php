<?php

namespace Kanboard\Plugin\UpdateRelatedTaskButton\Controller;

use Kanboard\Controller\BaseController;
use Kanboard\Core\Controller\AccessForbiddenException;

class UpdateRelatedTaskController extends BaseController
{
    public function confirm()
    {
        $task = $this->getTask();
        $user = $this->getUser();

        if ($user['username'] !== $task["assignee_username"]) {
            throw new AccessForbiddenException();
        }

        $this->response->html($this->template->render('UpdateRelatedTaskButton:update_related_task/update_related_task_confirm', array(
            'task' => $task,
            'user' => $user
        )));
    }

    public function updateRelatedTask()
    {
        $task = $this->getTask();
        $task_link = $this->getInternalTaskLink($task);
		echo($task_link)
        $this->checkCSRFParam();
 
		$user = $this->getUser();

        if ($user['username'] !== $task["assignee_username"]) {
            throw new AccessForbiddenException();
        }

        $values = array('id' => $task['id'], 'time_spent' => $task['time_spent'] + 0.5);

        if ($this->taskModificationModel->update($values, false)) {
            $this->flash->success(t("Interval added."));
        } else {
            $this->flash->failure(t("Unable to add interval."));
        }

        return $this->response->redirect($this->helper->url->to('TaskViewController', 'show', array('task_id' => $task['id'], 'project_id' => $task['project_id'])), true);
    }
}