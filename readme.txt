GA

Passcode: [1, 4, 2, 3, 5, 8, 9].

Chromosome: Mật khẩu hoặc những mật khẩu thử.

Gene: Mỗi số trong passcode.

Population: Tập hợp của các mật khẩu thử.

	- Population I: được tạo random từ các Chromosome.

	- Population tiếp theo: được tạo ra từ sự luật tiến hóa.

Generation: Mỗi lần lặp lại của một quần thể mới.

Fitness: Thang đánh giá.

Parents: Những Chromosome có Fitness cao trong Population hiện tại.

Crossover: Quá trình giao phối giữa Parents.

Children: Kết quả của quá trình giao phối.

	- Những cá thể Children này sẽ định hình Population mới 	cho thế hệ tiếp theo.

Elitism: Qúa trình đưa số lượng nhỏ Parents có điểm Fitness cao sang thế hệ tiếp theo.

Mutation: Chọn ngẫu nhiên Gene và thay đổi sang một cái mới.
	- Chỉ có 10% Children bị thay đổi.

=> Toàn bộ quá trình sẽ lặp lại N lần cho đến khi trùng với mật khẩu đã cho.

