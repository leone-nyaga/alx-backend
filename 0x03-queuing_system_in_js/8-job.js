const createPushNotificationsJobs = (jobs, queue) => {
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  jobs.forEach((jobData) => {
    const job = queue.create('push_notification_code_3', jobData);

    job.save((err) => {
      if (!err) {
        console.log(`Notification job created: ${job.id}`);
      }
    });

    job.on('complete', () => {
      if (!queue.testMode) {
        console.log(`Notification job ${job.id} completed`);
      }
    }).on('failed', (err) => {
      if (!queue.testMode) {
        console.log(`Notification job ${job.id} failed: ${err}`);
      }
    }).on('progress', (progress) => {
      if (!queue.testMode) {
        console.log(`Notification job ${job.id} ${progress}% complete`);
      }
    });
  });
};

export default createPushNotificationsJobs;
