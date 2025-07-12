import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from arduinobot_msgs.action import Fibonacci


class SimpleActionClient(Node):

    def __init__(self):
        # Gives the name of the node and initializes it
        super().__init__("simple_action_client")
        # What node is the action client, which interface are we using to communicate with it, what is the name of the action server
        self.action_client = ActionClient(self, Fibonacci, "fibonacci")
        self.goal = Fibonacci.Goal()
        self.goal.order = 10

        self.action_client.wait_for_server()
        # Sends goal to action server and receives a future variable
        self.future = self.action_client.send_goal_async(self.goal, feedback_callback=self.feedbackCallback)
        self.future.add_done_callback(self.responseCallback)

    # Runs after the goal is sent to the action server and checks whether or not it was accepted
    def responseCallback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected :(')
            return

        self.get_logger().info('Goal accepted :)')

        self.future = goal_handle.get_result_async()
        self.future.add_done_callback(self.resultCallback)

    # Exectuted at the end after the server has accepted and completed the action
    def resultCallback(self, future):
        result = future.result().result
        self.get_logger().info('Result: {0}'.format(result.sequence))
        rclpy.shutdown()


    def feedbackCallback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info('Received feedback: {0}'.format(feedback.partial_sequence))


def main(args=None):
    rclpy.init(args=args)
    action_client = SimpleActionClient()
    rclpy.spin(action_client)


if __name__ == '__main__':
    main()