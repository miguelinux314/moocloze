#!/usr/bin/env python3
"""Generate activity questions for several key concepts about TCP and UDP
for importing from Moodle.

Created for class "104353 Computer networks and internet" at the
Universitat Autònoma de Barcelona (UAB).
"""
__author__ = "Miguel Hernández-Cabronero"
__since__ = "2024/04/11"

import os
import numpy as np
import math
import moocloze


def get_reliability_question() -> moocloze.Question:
    return moocloze.Question(
        name="Reliabity in TCP/IP",
        contents=f"""
        <p>
        Which of the following concepts are related with <strong>reliability</strong> in networking?<br/>
        {moocloze.Multiresponse(
            correct_answers=['Data order is preserved', 'Data contents are preserved'],
            incorrect_answers=['Data is sent once', 'Data is sent more than once'],
            horizontal=False,
        )}
        </p>
        
        <p>
        Which of the following protocols provide reliability to their users?<br/>
        {moocloze.Multiresponse(
            correct_answers=["TCP"],
            incorrect_answers=["IP", "UDP"],
        )}
        </p>
        
        <p>
        We want to develop a network application with reliability (at any cost).
        We will use a single protocol or standard for communication. Which of the following 
        can we choose for this purpose?<br/>  
        {moocloze.Multiresponse(
            correct_answers=["TCP", "IP", "UDP", "Ethernet"],
            incorrect_answers=["None of the above"],
        )}
        </p>
        """.strip(),
        general_feedback="Applications can implement custom mechanisms to provide "
                         "reliability over IP, UDP, Ethernet or any other protocol. "
                         "If we don't want to implement them (which is normally "
                         "the case), we should use TCP.",
    )


def get_header_question() -> moocloze.Question:
    return moocloze.Question(
        name="TCP and UDP headers",
        contents=f"""
        <p>(All of the following sizes are in bytes)</p>
        <p>
        What is the minimum size of a UDP header? {moocloze.Numerical(8)}<br/>
        What is the maximum size of a UDP header? {moocloze.Numerical(8)}<br/>
        What is the minimum (total) size of a user datagram? {moocloze.Numerical(8)}<br/>
        What is the maximum (total) size of a user datagram? {moocloze.Numerical(2 ** 16 - 1)}<br/>
        </p>
        <p>
        What is the minimum size of a TCP header? {moocloze.Numerical(20)}<br/>
        What is the maximum size of a TCP header without options? {moocloze.Numerical(20)}<br/>
        Can a TCP header be larger than 20 bytes? 
        {moocloze.Multichoice(
            correct_answer="Yes",
            incorrect_answers=["No"],
            display_mode=moocloze.Multichoice.DisplayMode.HORIZONTAL_BUTTONS)}<br/>
        What is the minimum size of the data payload in a TCP segment? {moocloze.Numerical(0)}<br/>
        </p>
        <p></p>
        """,
        general_feedback="While UDP headers are small and fixed length, "
                         "TCP are larger and can contain optional fields (variable length).<br/>"
                         "Also, it is perfectly valid to send0 data bytes in a user datagram or "
                         "a segment.",
    )


def get_ordering_question() -> moocloze.Question:
    return moocloze.Question(
        name="Data ordering",

        contents=f"""
        <p>
        Which of the following protocols/standards contains one or more fields 
        in their header to keep track of the ordering of the data?<br/>
        {moocloze.Multiresponse(
            correct_answers=["TCP"],
            incorrect_answers=["UDP", "Ethernet", "IP"]
        )}
        </p>
        
        <p>
        Can an application implement a custom mechanism to keep track 
        of the ordering of the data? 
        {moocloze.Multiresponse(
            correct_answers=["Yes, but it is a pain",
                             "Yes, but it is not always trivial",
                             "Yes, but it is easier to delegate to TCP"],
            incorrect_answers=[],
        )}
        </p>
        """,

        general_feedback=
        "IP contains an offset field, but it is only used for fragmentation, "
        "not to order different IP datagrams.<br/>"
        "An application can always use a custom mechanism to provide "
        "data ordering (but we can employ TCP if we don't want to implement such mechanism).",
    )


def get_retransmission_question() -> moocloze.Question:
    return moocloze.Question(
        name="Retransmission",
        contents=f"""
        <p>
        A server sends a segment with some data to a client over a established TCP connection. 
        That client does not need to send any data to the server. 
        Check all that apply:<br/>
        {moocloze.Multiresponse(
            correct_answers=[
                "The client will acknowledge the correct reception of the data"
            ],
            incorrect_answers=[
                "The server cannot know whether the client received the data",
                "The server will retransmit the data until the client needs to send some data"],
            horizontal=False,
            shuffle=False,
        )}
        </p>
        
        <p>
        A clients sends a user datagram with some data to a server over UDP. 
        That server does not need to send any data to the client. 
        Check all that apply:<br/>
        {moocloze.Multiresponse(
            correct_answers=[
                "The server cannot know whether the client received the data",
            ],
            incorrect_answers=[
                "The client will acknowledge the correct reception of the data",
                "The server will retransmit the data until the client needs to send some data"],
            horizontal=False,
            shuffle=False,
        )}
        </p>
        """,
        general_feedback="Positive acknowledgement happens only in TCP",
    )


def get_port_question() -> moocloze.Question:
    return moocloze.Question(
        name="TCP and UDP ports",
        contents=f"""
        <p>
        What of the following pieces of information are used by 
        a UDP server to know to what process some data needs to be delivered?<br/>
        {moocloze.Multiresponse(
            correct_answers=["The destination port"],
            incorrect_answers=["The source IP", "The source MAC", "The source port",
                               "The destination IP", "The destination MAC"],
            horizontal=True,
        )}
        </p>
        
        <p>
        What of the following pieces of information are used by 
        a TCP server to know to what process some data needs to be delivered?<br/>
        {moocloze.Multiresponse(
            correct_answers=["The source IP", "The destination IP",
                             "The source port", "The destination port"],
            incorrect_answers=["The source MAC", "The destination MAC"],
            horizontal=True,
        )}
        </p>
        
        <p>
        Can two processes listen for UDP data on the same port?
        {moocloze.Multichoice(
            correct_answer="No", incorrect_answers=["Yes"],
            display_mode=moocloze.Multichoice.DisplayMode.HORIZONTAL_BUTTONS)}<br/>
        Can two processes listen for TCP connections on the same port?
        {moocloze.Multichoice(
            correct_answer="No", incorrect_answers=["Yes"],
            display_mode=moocloze.Multichoice.DisplayMode.HORIZONTAL_BUTTONS)}<br/>
        Can two processes receive TCP data on the same port?
        {moocloze.Multichoice(
            correct_answer="Yes", incorrect_answers=["No"],
            display_mode=moocloze.Multichoice.DisplayMode.HORIZONTAL_BUTTONS)}<br/>
        Is it possible to have a server listen for UDP data on a port P, 
        and also for TCP connections on the same port? 
        {moocloze.Multichoice(
            correct_answer="Yes", incorrect_answers=["No"],
            display_mode=moocloze.Multichoice.DisplayMode.HORIZONTAL_BUTTONS)}<br/>
        </p>
        
        <p>
        What is the largest reserved port that requires admin (root) privileges 
        to be listened to? {moocloze.Numerical(1023)}<br/>
        What is the largest TCP port a server can listen on for connections? 
        {moocloze.Numerical(2 ** 16 - 1)}<br/> 
        What is the largest UDP port a server can receive data on? 
        {moocloze.Numerical(2 ** 16 - 1)}<br/>
        </p>
        """,
        general_feedback="In TCP, connections are identified by a pair of endpoints,"
                         "i.e., 4 values: (IP,PORT)->(IP,PORT). In UDP, we only have "
                         "the destination port and no connections. However, TCP and "
                         "UDP ports are totally independent."
    )


def generate_tcp_vs_upd_set(
        output_path=os.path.join(os.path.dirname(__file__), "tcp_vs_udp_questions.xml")):
    """Generate a set of ~test questions about TCP vs UDP.
    """
    questions = []

    questions.append(get_reliability_question())
    questions.append(get_header_question())
    questions.append(get_ordering_question())
    questions.append(get_retransmission_question())
    questions.append(get_port_question())

    moocloze.questions_to_xml_file(questions, output_path=output_path)


def generate_mss_from_mtu_questions(
        output_path=os.path.join(os.path.dirname(__file__), "mss_mtu_questions.xml")):
    """Generate a bunch of random questions about MSS based on the MTU.
    """
    questions = []
    for MTU1 in np.linspace(100, 2 ** 16 - 1, 10):
        for MTU2 in np.linspace(105, 2 ** 16 - 1, 11):
            MTU1 = int(MTU1)
            MTU2 = int(MTU2)
            MSS1 = MTU1 - 40
            MSS2 = MTU2 - 40

            questions.append(moocloze.Question(
                name=f"MSS for MTU {MTU1}",
                contents=f"What MSS would be advertised by a host on a network"
                         f"with MTU={MTU1}? {moocloze.Numerical(MSS1)}<br/>"
                         f"What MTU is most likely for a host that advertises "
                         f"an MSS of {MSS2}? {moocloze.Numerical(MTU2)}<br/>"
                         f"If a host A advertises an MSS of {MTU1} and "
                         f"host B replies with an MSS of {MSS2}, "
                         f"what MSS will they agree on? {moocloze.Numerical(min(MTU1, MSS2))}",
                general_feedback="TCP and IP headers are 20 bytes each if they carry no "
                                 "options.",
            ))

    moocloze.questions_to_xml_file(questions, output_path=output_path)


def generate_mss_window_questions(
        output_path=os.path.join(os.path.dirname(__file__), "mss_window_questions.xml")):
    questions = []

    for rtt in np.linspace(0.01, 2, 7):
        for mss in np.linspace(40, 1460, 7):
            for bytes_per_second in np.linspace(1000, 10000, 7):
                mss = int(mss)
                bytes_per_second = int(bytes_per_second)
                rtt = round(rtt, 5)

                network_overhead_bytes = 48
                bytes_transmitted_during_rtt = math.floor(rtt * bytes_per_second)
                mss_segment_total_size = mss + 20 + 20 + network_overhead_bytes
                mss_segment_transmission_time = mss_segment_total_size / bytes_per_second
                segments_sent_during_rtt = math.ceil(
                    bytes_transmitted_during_rtt / mss_segment_total_size)
                minimum_window_size = segments_sent_during_rtt * mss

                questions.append(moocloze.Question(
                    name=f"Optimal window (RTT={rtt}s, MSS={mss}, bw={bytes_per_second} bytes/s",
                    contents=f"""
                    <p>
                    A host A has an ongoing TCP connection with host B,
                    using an MSS of {mss} bytes.
                    <br/>
                    Both hosts are on the same network, which allows
                    simultaneous transmission of {bytes_per_second} bytes/s from A to B,
                    and {bytes_per_second} bytes/s from B to A.<br/>
                    <br/>
                    From the moment host A starts sending a segment to host B
                    to the moment host B receives an answer, {rtt}&nbsp;s pass.
                    Assume this time, called <strong>round-trip time (RTT)</strong>
                    is constant for all messages.<br/>
                    </p>
                    
                    <p>
                    How many bytes can A send to B in this RTT?
                    (assume only full bytes can be sent at a time) 
                    {moocloze.Numerical(bytes_transmitted_during_rtt)}<br/>
                    </p>
                    
                    <p>
                    How long does it take to send a segment reaching the MSS
                    from A to B with this bandwidth? Assume no options are used at the
                    TCP or IP level, and that the network layer adds an overhead of 
                    {network_overhead_bytes} bytes. 
                    {moocloze.Numerical(mss_segment_transmission_time, tolerance=0.001)} <br/>
                    </p>
                    
                    <p>
                    How many segments can be sent (totally or partially) 
                    from A to B until the first acknowledgement is received? Assume
                    only segments meeting the MSS are used. 
                    {moocloze.Numerical(segments_sent_during_rtt)}
                    </p> 
                    
                    <p>
                    What is the minimum window size that B must have advertised so that 
                    A can send segments to B without interruption before the first acknowledgement
                    is received?
                    {moocloze.Numerical(minimum_window_size)}
                    </p>
                    """,
                    general_feedback=
                    "This problem is slightly more complicated than average, but "
                    "you should be able to solve it if you distinguish between "
                    "data bytes and overhead (i.e., header) bytes.<br/>"
                    "Note that:"
                    "<ul>"
                    "<li>The total number of bytes transmitted during the "
                    "RTT are calculated using the floor function because only "
                    "full bytes are transmitted.</li>"
                    "<li>The number of segments transmitted during the RTT "
                    "is calculated using the ceiling function because A wants to "
                    f"send only full segments (MSS={mss} bytes). Therefore, before "
                    f"sending the last segment before the ACK, the window must be "
                    f"large enough to accommodate for all MSS bytes.</li>"
                    "</ul>",
                ))

    moocloze.questions_to_xml_file(questions, output_path=output_path)


if __name__ == "__main__":
    generate_tcp_vs_upd_set()
    generate_mss_from_mtu_questions()
    generate_mss_window_questions()
