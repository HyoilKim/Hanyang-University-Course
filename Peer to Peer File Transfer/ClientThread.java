import java.io.*;
import java.net.Socket;
import java.util.Random;

class ClientThread extends Thread{
	// ************** Server 스레드로 부터 chunk를 3개 읽은 후 자신의 파일에 저장  ************* //
	// **************        지역 변수는 FileManager와  의미 동일                    ************* //
	int port;
	int peerNum;
	int ownNum;
	byte[] buffer;
	boolean isFirst;
	String ip;
	String bitMap;
	FileManager fileManager;
	final int BUFFER_SIZE = 10240;
		
	public ClientThread(FileManager fileManager) {
		this.fileManager = fileManager;
		this.buffer = new byte[10240];
	}

	public void run() {	
    	String filename = fileManager.getFilename();
    	String filePath = fileManager.getFilePath();
        File file = new File(filePath+filename);
        
		while(true) {
			fileManager.setConnectPeerNum();		// 다음에 연결 할 Peer선택(순차적)
			ownNum = fileManager.getOwnNum();		// 다음 PeerNum 저장
	        ip = fileManager.getPeerIp();			// 다음 Peer IP 저장
	        port = fileManager.getPeerPort();		// 다음 Peer port 저장
	        fileManager.initNumOfDown();			// 다운로드 횟수 3 설정
	        
	        try {
	    		// ************** 서버와 연결, 청크 전송&받기 준비************* //
	        	Socket receiveSocket = new Socket(ip, port);		        
	        	System.out.println(fileManager.portArr[peerNum] + " client thread connect with " + port);
		      
		        InputStream is = receiveSocket.getInputStream();	
				OutputStream os = receiveSocket.getOutputStream();
				DataInputStream streamFromSender = new DataInputStream(is);
		        DataOutputStream streamToSender = new DataOutputStream(os);
		        RandomAccessFile raf = new RandomAccessFile(file, "rw");
		        String messageFromSender = "";
		        
				// ************** 연결된 Peer에 파일이 있는지 확인 ************* //
		        if(streamFromSender.readUTF().equals("no file")) {
		        	Thread.sleep(1000);
		        	System.out.println(fileManager.portArr[ownNum] + " client thread quit with" + port);
		        	receiveSocket.close();
		        	continue;
		        }
		        
		        // ************** 자신의 파일이 없는 경우 bitMap초기화(메인에서 미뤄뒀던 것) ************* //
		        if (fileManager.getBitMap() == "") {
		        	streamToSender.writeUTF("want to chunkNum");
		        	Thread.sleep(1000);
		        	int chunkNum = Integer.parseInt(streamFromSender.readUTF());
		        	Thread.sleep(1000);
		        	fileManager.chunkNum = chunkNum;
					fileManager.initLeecherBitMap();
		        } else {
		        	streamToSender.writeUTF("don't want to chunkNum");
		        	Thread.sleep(1000);
		        	streamFromSender.readUTF();
		        }
		        
		        // ************** 다른 Peer로 부터 3번 다운  ************* //
		        while(fileManager.getNumDown() < 3) {
		        	System.out.println("****** sending receiver's bitMap ******");
		        	// ************** 다른 Peer에 내가 필요한 chunk가 있는지 확인 후 Get************* //
			        bitMap = fileManager.getBitMap();
		        	streamToSender.writeUTF(bitMap);
		        	Thread.sleep(1000);
		        	messageFromSender = streamFromSender.readUTF();
		        	
			        if (messageFromSender.equals("server thread have a chunk")) {
			        	System.out.println("****** sender has chunks ******");
			        	int missIndex = Integer.parseInt(streamFromSender.readUTF());	// 내가 가지고 있지 않은 chunk에 대한 bitMap의 index 
			        	streamToSender.flush();
			        	streamToSender.writeUTF("thank u missIndex");
			        	Thread.sleep(1000);    
			            
			        	int size = Integer.parseInt(streamFromSender.readUTF());		// 연결된 Peer가 보내는 chunk의 크기
			        	streamToSender.writeUTF("thank u size");
			        	Thread.sleep(1000);
			        	
			            buffer = new byte[10240];
			        	streamFromSender.read(buffer);
			        	Thread.sleep(1000);
			            raf.seek(missIndex*BUFFER_SIZE);								// chunk 쓰는 위치 변경

		        		FileOutputStream fos = new FileOutputStream(raf.getFD());		// chunk 기록
		        		fos.write(buffer, 0, size);
		        		
			            fileManager.updateBitMap(missIndex);							// 서버로 부터 chunk를 받아서 내 파일에 기록했기 때문에 bitMap 수정
				        fileManager.plusNumOfDown();
			        } else {
			        	if (fileManager.isChunkFull()) {								// chunk가 가득 찼다면 Seeder로 설정
				        	fileManager.isSeeder[fileManager.ownNum] = true;
					    }
			        	break;
			        }
		        }
		        // Seeder인 경우에 Thread종료
		        if (fileManager.isSeeder()) {	
		        	System.out.println("All chunks download completed");
		        	receiveSocket.close();
		        	break;
			    }
	        	receiveSocket.close();
				raf.close();
		    } catch (FileNotFoundException e) {
				e.printStackTrace();
			}catch(Exception e){
				e.getStackTrace();
		    }
		}
	}
}