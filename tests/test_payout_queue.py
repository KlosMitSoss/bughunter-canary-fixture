import unittest

from payout_queue import PayoutQueue


class PayoutQueueTests(unittest.TestCase):
    def test_one_ticket_pays_once(self) -> None:
        queue = PayoutQueue()
        queue.deposit("alice", 20)
        ticket = queue.request_withdrawal("alice", 7)
        payments: list[tuple[str, int]] = []

        queue.settle(ticket, lambda owner, amount: payments.append((owner, amount)))

        self.assertEqual(payments, [("alice", 7)])
        self.assertEqual(queue.balance("alice"), 13)
        self.assertEqual(queue.reserved("alice"), 0)
        with self.assertRaises(KeyError):
            queue.settle(ticket, lambda owner, amount: payments.append((owner, amount)))
        self.assertEqual(payments, [("alice", 7)])

    def test_pending_tickets_cannot_exceed_balance(self) -> None:
        queue = PayoutQueue()
        queue.deposit("alice", 10)
        queue.request_withdrawal("alice", 7)

        with self.assertRaises(ValueError):
            queue.request_withdrawal("alice", 4)
        self.assertEqual(queue.reserved("alice"), 7)


if __name__ == "__main__":
    unittest.main()
