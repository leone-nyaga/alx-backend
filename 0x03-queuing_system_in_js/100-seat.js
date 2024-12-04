import express from 'express';
import redis from 'redis';
import kue from 'kue';
import { promisify } from 'util';

// Redis client setup
const client = redis.createClient();
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Kue queue setup
const queue = kue.createQueue();

// Function to reserve seats
const reserveSeat = async (number) => {
  await setAsync('available_seats', number);
};

// Function to get the current available seats
const getCurrentAvailableSeats = async () => {
  const seats = await getAsync('available_seats');
  return seats !== null ? parseInt(seats, 10) : 0;
};

// Initialize available seats and reservation status
let reservationEnabled = true;
reserveSeat(50);

// Express app setup
const app = express();
const port = 1245;

// Route to get the available seats
app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  return res.json({ numberOfAvailableSeats: availableSeats });
});

// Route to reserve a seat
app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    return res.json({ status: 'Reservation are blocked' });
  }

  const job = queue.create('reserve_seat')
    .save((err) => {
      if (!err) {
        return res.json({ status: 'Reservation in process' });
      }
      return res.json({ status: 'Reservation failed' });
    });

  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  }).on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err.message}`);
  });
  return undefined;
});

// Route to process the queue
app.get('/process', (req, res) => {
  res.json({ status: 'Queue processing' });

  queue.process('reserve_seat', async (job, done) => {
    try {
      const currentSeats = await getCurrentAvailableSeats();

      if (currentSeats <= 0) {
        reservationEnabled = false;
        done(new Error('Not enough seats available'));
        return;
      }

      const newSeats = currentSeats - 1;
      await reserveSeat(newSeats);

      if (newSeats === 0) {
        reservationEnabled = false;
      }

      done();
    } catch (err) {
      done(err);
    }
  });
  return undefined;
});

// Start the server
app.listen(port, () => {
  console.log(`Server is listening on port ${port}`);
});
